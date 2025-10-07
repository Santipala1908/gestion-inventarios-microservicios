from locust import HttpUser, task, between
import random

class InventoryUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def check_inventory(self):
        """Consulta el stock de un producto existente"""
        # Cambia el rango según tus IDs reales en la BD
        product_id = random.randint(1, 5)
        self.client.get(f"/inventory/{product_id}")

    @task(2)
    def create_movement_in(self):
        """Registra un movimiento de entrada (IN)"""
        data = {
            "type": "IN",
            "qty": random.randint(1, 5),
            "product_id": random.randint(1, 5),
            "warehouse_id": "MAIN"
        }
        self.client.post("/inventory/movements", json=data)

    @task(1)
    def create_movement_out(self):
        """Registra un movimiento de salida (OUT)"""
        data = {
            "type": "OUT",
            "qty": random.randint(1, 3),
            "product_id": random.randint(1, 5),
            "warehouse_id": "MAIN"
        }
        self.client.post("/inventory/movements", json=data)
