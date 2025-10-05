from flask import Flask, request, jsonify
from datetime import datetime
from pymongo import MongoClient, ASCENDING
import os, requests
from bson import ObjectId  # 👈 necesario para convertir ObjectId

# =======================
# CONFIGURACIÓN BASE
# =======================
MONGO_URI    = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DBNAME = os.getenv("MONGO_DB", "inventory_db")
PRODUCTS_URL = os.getenv("PRODUCTS_URL", "http://localhost:8000/api")

COL_BAL = "inventory_balances"
COL_MOV = "inventory_movements"

app = Flask(__name__)
client = MongoClient(MONGO_URI)
db = client[MONGO_DBNAME]

# =======================
# ÍNDICES
# =======================
db[COL_BAL].create_index([("product_id", ASCENDING), ("warehouse_id", ASCENDING)], unique=True)
db[COL_MOV].create_index([("product_id", ASCENDING), ("warehouse_id", ASCENDING), ("created_at", ASCENDING)])


def now_utc():
    return datetime.utcnow()


# =======================
# FUNCIONES AUXILIARES
# =======================
def ensure_balance(product_id: str, warehouse_id: str, sku_snapshot: str | None = None):
    base = {"on_hand": 0, "reserved": 0}
    if sku_snapshot is not None:
        base["sku_snapshot"] = sku_snapshot
    db[COL_BAL].update_one(
        {"product_id": product_id, "warehouse_id": warehouse_id},
        {"$setOnInsert": base},
        upsert=True
    )


def resolve_product(product_id: str | None, sku: str | None):
    """
    Devuelve (product_id_str, sku_str) si existe en Products; en error -> (None, 'codigo_error').
    """
    try:
        if product_id is not None:
            r = requests.get(f"{PRODUCTS_URL}/products/{product_id}/exists", timeout=2)
        elif sku:
            r = requests.get(f"{PRODUCTS_URL}/products/exists", params={"sku": sku}, timeout=2)
        else:
            return None, "missing_id_or_sku"

        if r.status_code >= 400:
            return None, "catalog_unavailable"
        data = r.json()
        if not data.get("exists"):
            return None, "product_not_found"
        pid  = str(data.get("id"))
        psku = data.get("sku")
        psku = str(psku) if psku is not None else None
        return (pid, psku), None
    except Exception:
        return None, "catalog_unavailable"


# 🔧 función auxiliar para limpiar ObjectId y datetime
def clean_doc(doc):
    """Convierte ObjectId y datetime a string antes de enviar JSON"""
    clean = {}
    for k, v in doc.items():
        if isinstance(v, ObjectId):
            clean[k] = str(v)
        elif isinstance(v, datetime):
            clean[k] = v.isoformat()
        else:
            clean[k] = v
    return clean


# =======================
# ENDPOINTS
# =======================
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/inventory/<product_id>")
def get_inventory(product_id):
    wh = request.args.get("warehouse", "MAIN")
    doc = db[COL_BAL].find_one({"product_id": str(product_id), "warehouse_id": wh}, {"_id": 0})
    if not doc:
        doc = {"product_id": str(product_id), "warehouse_id": wh, "on_hand": 0, "reserved": 0}
    doc["available"] = doc["on_hand"] - doc["reserved"]
    return jsonify(doc)


@app.get("/inventory/movements")
def list_movements():
    pid = request.args.get("product_id")
    wh  = request.args.get("warehouse")
    q = {}
    if pid: q["product_id"] = str(pid)
    if wh:  q["warehouse_id"] = wh

    docs = list(db[COL_MOV].find(q).sort("created_at", -1).limit(200))
    clean_docs = [clean_doc(d) for d in docs]
    return jsonify(clean_docs)


@app.post("/inventory/movements")
def create_movement():
    """
    Acepta:
      - Por ID:  { "product_id": 25, "type":"IN", "qty":10, "warehouse_id":"MAIN" }
      - Por SKU: { "sku":"SKU-001", "type":"RESERVE", "qty":3, "warehouse_id":"MAIN" }
    Reglas: IN | OUT | RESERVE | RELEASE
    """
    b = request.get_json(force=True)

    # Validación de entrada
    try:
        mtype = str(b["type"]).upper()
        qty   = int(b["qty"])
    except Exception:
        return {"error":"invalid_body"}, 400
    if mtype not in {"IN","OUT","RESERVE","RELEASE"}:
        return {"error":"invalid_type"}, 400
    if qty <= 0:
        return {"error":"qty_must_be_positive"}, 400

    wh    = str(b.get("warehouse_id", "MAIN"))
    ref_t = b.get("ref_type")
    ref_i = b.get("ref_id")

    # Resolver producto contra Products
    raw_pid = b.get("product_id")
    raw_sku = b.get("sku")
    resolved, err = resolve_product(str(raw_pid) if raw_pid is not None else None,
                                    str(raw_sku) if raw_sku else None)
    if err:
        return {"error": err}, 422
    pid, sku_snapshot = resolved  # pid como string

    # Asegurar documento de saldos
    ensure_balance(pid, wh, sku_snapshot)

    # Operaciones atómicas
    if mtype == "IN":
        db[COL_BAL].update_one(
            {"product_id": pid, "warehouse_id": wh},
            {"$inc": {"on_hand": qty}, "$set": {"sku_snapshot": sku_snapshot}}
        )
    elif mtype == "OUT":
        res = db[COL_BAL].update_one(
            {"product_id": pid, "warehouse_id": wh, "on_hand": {"$gte": qty}},
            {"$inc": {"on_hand": -qty}}
        )
        if res.matched_count != 1:
            return {"error":"insufficient_stock"}, 409
    elif mtype == "RESERVE":
        res = db[COL_BAL].update_one(
            {
                "product_id": pid,
                "warehouse_id": wh,
                "$expr": {"$gte": [{"$subtract": ["$on_hand", "$reserved"]}, qty]}
            },
            {"$inc": {"reserved": qty}}
        )
        if res.matched_count != 1:
            return {"error":"insufficient_available"}, 409
    else:  # RELEASE
        res = db[COL_BAL].update_one(
            {"product_id": pid, "warehouse_id": wh, "reserved": {"$gte": qty}},
            {"$inc": {"reserved": -qty}}
        )
        if res.matched_count != 1:
            return {"error":"insufficient_reserved"}, 409

    # Registrar movimiento
    mv = {
        "product_id": pid,
        "warehouse_id": wh,
        "sku_snapshot": sku_snapshot,
        "type": mtype,
        "qty": qty,
        "ref_type": ref_t,
        "ref_id": ref_i,
        "created_at": now_utc()
    }
    ins = db[COL_MOV].insert_one(mv)
    mv["_id"] = str(ins.inserted_id)

    return jsonify(clean_doc(mv)), 201


# =======================
# MAIN
# =======================
if __name__ == "__main__":
    # Usa env vars para apuntar a tus servicios reales
    #   MONGO_URI="mongodb://localhost:27017"
    #   MONGO_DB="inventory_db"
    #   PRODUCTS_URL="http://localhost:8000/api"
    app.run(debug=True, port=int(os.getenv("PORT", 8003)))
