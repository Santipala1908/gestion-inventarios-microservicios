from locust import HttpUser, task, between
import random

class SecurityUser(HttpUser):
    wait_time = between(1, 3)  # segundos entre peticiones

    # Credenciales de prueba
    test_email = "usuario_prueba@example.com"
    test_password = "12345678"

    @task(2)
    def register_user(self):
        """Simula el registro de nuevos usuarios"""
        email = f"user{random.randint(1, 10000)}@test.com"
        data = {
            "name": f"Usuario {random.randint(1, 10000)}",
            "email": email,
            "password": self.test_password
        }
        self.client.post("/api/register", json=data)

    @task(3)
    def login_user(self):
        """Simula inicios de sesión"""
        data = {
            "email": self.test_email,
            "password": self.test_password
        }
        self.client.post("/api/login", json=data)

    @task(1)
    def get_users(self):
        """Consulta lista de usuarios registrados"""
        self.client.get("/api/users")

    @task(1)
    def health_check(self):
        """Verifica que el servicio esté activo"""
        self.client.get("/api/user")
