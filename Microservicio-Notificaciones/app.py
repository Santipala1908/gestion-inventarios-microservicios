from flask import Flask, request, jsonify
import smtplib, os, requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# ==============================
# 🔹 Cargar variables del archivo .env
# ==============================
load_dotenv()

app = Flask(__name__)

# ==============================
# 🔹 Configuración del servidor SMTP (correo)
# ==============================
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
USERS_URL = os.getenv("USERS_URL", "http://localhost:8000/api/users")

# ==============================
# 🔹 Función para enviar correos
# ==============================
def send_email(to_address, subject, message):
    """Envía un correo electrónico simple usando Gmail"""
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = to_address
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "html"))

        # Conectar con el servidor SMTP y enviar el correo
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)

        print(f"✅ Correo enviado a {to_address}")
        return True
    except Exception as e:
        print(f"❌ Error al enviar correo a {to_address}: {e}")
        return False


# ==============================
# 🔹 Endpoint de prueba (verifica que Flask esté activo)
# ==============================
@app.get("/health")
def health():
    return jsonify({"status": "ok"})


# ==============================
# 🔹 Endpoint principal para enviar notificaciones por correo
# ==============================
@app.post("/notifications/email")
def send_notification():
    """
    Envía un correo a un usuario específico o a todos los registrados en Laravel.
    Ejemplo de JSON:
    {
      "to": "usuario@gmail.com",
      "subject": "Prueba de correo",
      "message": "Hola, este es un correo de prueba."
    }

    Si no se incluye "to", se enviará a todos los correos registrados en USERS_URL.
    """
    data = request.get_json(force=True)
    subject = data.get("subject", "Notificación del sistema")
    message = data.get("message", "Sin contenido")
    single_to = data.get("to")

    recipients = []

    # Si se especifica un destinatario
    if single_to:
        recipients = [single_to]
    else:
        # Obtener lista de usuarios desde Laravel
        try:
            response = requests.get(USERS_URL, timeout=5)
            if response.status_code == 200:
                usuarios = response.json()
                recipients = [u["email"] for u in usuarios if u.get("email")]
            else:
                return jsonify({"error": "No se pudo obtener la lista de usuarios"}), 502
        except Exception as e:
            print("❌ Error conectando con Laravel:", e)
            return jsonify({"error": "Servicio de usuarios no disponible"}), 503

    # Enviar correos
    enviados = []
    for email in recipients:
        if send_email(email, subject, message):
            enviados.append(email)

    return jsonify({
        "status": "completed",
        "total_sent": len(enviados),
        "recipients": enviados
    }), 200


# ==============================
# 🔹 Ejecutar el microservicio
# ==============================
if __name__ == "__main__":
    app.run(debug=True, port=8005)
