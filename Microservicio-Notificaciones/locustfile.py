from locust import HttpUser, task, between
import random

class NotificationUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def send_email(self):
        data = {
            "subject": f"Prueba carga #{random.randint(1, 1000)}",
            "message": "Mensaje de prueba de rendimiento",
            "to": "f3866111@gmail.com"  
        }
        self.client.post("/notifications/email", json=data)

