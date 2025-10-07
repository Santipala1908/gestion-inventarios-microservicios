from flask import Flask, jsonify, request, send_file
from pymongo import MongoClient
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import os, requests
from bson import ObjectId

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "inventory_db")
PRODUCTS_URL = os.getenv("PRODUCTS_URL", "http://localhost:8000/api")

app = Flask(__name__)
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

def clean_doc(doc):
    """Convierte ObjectId y datetime a string"""
    out = {}
    for k, v in doc.items():
        if isinstance(v, ObjectId):
            out[k] = str(v)
        elif isinstance(v, datetime):
            out[k] = v.isoformat()
        else:
            out[k] = v
    return out

def fetch_product(pid: str):
    """Obtiene info del producto desde Laravel"""
    try:
        r = requests.get(f"{PRODUCTS_URL}/products/{pid}")
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return {"name": "Desconocido", "category": "-", "price": 0}

@app.get("/reports/inventory/pdf")
def report_inventory_pdf():
    """Genera PDF con resumen del inventario"""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Reporte de Inventario")
    pdf.drawString(200, 750, "📦 REPORTE DE INVENTARIO")
    pdf.drawString(50, 730, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    cursor = db["inventory_balances"].find()
    y = 700
    for doc in cursor:
        prod = fetch_product(doc["product_id"])
        pdf.drawString(50, y, f"{prod['name']} ({prod['category']}) - Stock: {doc.get('on_hand',0)}")
        y -= 20
        if y < 50:
            pdf.showPage()
            y = 750
    pdf.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="reporte_inventario.pdf", mimetype="application/pdf")

@app.get("/reports/inventory/excel")
def report_inventory_excel():
    """Genera Excel con resumen del inventario"""
    cursor = list(db["inventory_balances"].find())
    data = []
    for doc in cursor:
        prod = fetch_product(doc["product_id"])
        data.append({
            "ID Producto": doc["product_id"],
            "Nombre": prod["name"],
            "Categoría": prod["category"],
            "Stock": doc.get("on_hand", 0),
            "Reservado": doc.get("reserved", 0),
            "Disponible": doc.get("on_hand", 0) - doc.get("reserved", 0),
            "Bodega": doc.get("warehouse_id")
        })
    df = pd.DataFrame(data)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Inventario")
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="reporte_inventario.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.get("/reports/users/excel")
def report_users_excel():
    """Reporte de usuarios (ejemplo: obtenido del microservicio de seguridad)"""
    users = [
        {"id": 1, "name": "Admin", "email": "admin@empresa.com", "role": "Administrador"},
        {"id": 2, "name": "Juan Pérez", "email": "juan@empresa.com", "role": "Vendedor"},
    ]
    df = pd.DataFrame(users)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Usuarios")
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="usuarios.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.get("/reports/sales/pdf")
def report_sales_pdf():
    """Reporte de ventas simulado (ejemplo dinámico)"""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Reporte de Ventas")
    pdf.drawString(200, 750, "💰 REPORTE DE VENTAS")
    pdf.drawString(50, 730, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    ventas = [
        {"id": 1, "cliente": "Juan Pérez", "total": 120.5, "fecha": "2025-10-01"},
        {"id": 2, "cliente": "María López", "total": 89.9, "fecha": "2025-10-03"},
    ]

    y = 700
    for v in ventas:
        pdf.drawString(50, y, f"Venta #{v['id']} | Cliente: {v['cliente']} | Total: ${v['total']} | Fecha: {v['fecha']}")
        y -= 20
    pdf.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="ventas.pdf", mimetype="application/pdf")

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", 8004)))
