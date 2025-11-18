from flask import Flask, request, Response, jsonify
import os
import requests

app = Flask(__name__)

# URLs base de los microservicios
PRODUCTS_URL      = os.getenv("PRODUCTS_URL",      "http://localhost:8000/api")  # CRUD productos (Laravel)
INVENTORY_URL     = os.getenv("INVENTORY_URL",     "http://localhost:8003")      # Inventarios (Flask)
REPORTS_URL       = os.getenv("REPORTS_URL",       "http://localhost:8004")      # Reportes (Flask)
NOTIFICATIONS_URL = os.getenv("NOTIFICATIONS_URL", "http://localhost:8005")      # Notificaciones (Flask)
SECURITY_URL      = os.getenv("SECURITY_URL",      "http://localhost:8001/api")  # Seguridad (Laravel)


def forward_request(base_url: str, path_prefix: str = ""):
    """
    Reenvía la petición actual al microservicio correspondiente.
    - base_url: URL base del microservicio (ej: http://localhost:8003)
    - path_prefix: prefijo del path en el microservicio (ej: /inventory)
    """
    extra_path = request.view_args.get("path", "")
    if extra_path:
        url = f"{base_url}{path_prefix}/{extra_path}"
    else:
        url = f"{base_url}{path_prefix}"

    # Copiar headers excepto Host
    headers = {k: v for k, v in request.headers if k.lower() != "host"}
    data = request.get_data()
    params = request.args

    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            cookies=request.cookies,
            allow_redirects=False,
            timeout=10
        )
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Microservicio no disponible", "detail": str(e)}), 503

    excluded = {"content-encoding", "content-length", "transfer-encoding", "connection"}
    response_headers = [
        (name, value) for name, value in resp.headers.items()
        if name.lower() not in excluded
    ]

    return Response(resp.content, resp.status_code, response_headers)


@app.get("/health")
def health():
    return jsonify({"status": "api-gateway-ok"}), 200


# ------------ CRUD de productos (Laravel) ------------
# Equivalente a http://localhost:8000/api/products...
@app.route("/api/products", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/api/products/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def gateway_products(path):
    return forward_request(PRODUCTS_URL, "/products")


# ------------ Inventarios (Flask) ------------
# Equivalente a http://localhost:8003/inventory...
@app.route("/api/inventory", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/api/inventory/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def gateway_inventory(path):
    return forward_request(INVENTORY_URL, "/inventory")


# ------------ Reportes (Flask) ------------
# Equivalente a http://localhost:8004/reports...
@app.route("/api/reports", defaults={"path": ""}, methods=["GET"])
@app.route("/api/reports/<path:path>", methods=["GET"])
def gateway_reports(path):
    return forward_request(REPORTS_URL, "/reports")


# ------------ Notificaciones (Flask) ------------
# Equivalente a http://localhost:8005/notifications...
@app.route("/api/notifications", defaults={"path": ""}, methods=["POST"])
@app.route("/api/notifications/<path:path>", methods=["POST"])
def gateway_notifications(path):
    return forward_request(NOTIFICATIONS_URL, "/notifications")


# ------------ Seguridad (Laravel) ------------
# Equivalente a http://localhost:8001/api/users...
@app.route("/api/users", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/api/users/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def gateway_users(path):
    return forward_request(SECURITY_URL, "/users")


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080))
    )
