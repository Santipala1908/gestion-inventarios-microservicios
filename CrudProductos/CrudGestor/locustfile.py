from locust import HttpUser, task, between
import random

class ProductUser(HttpUser):
    wait_time = between(1, 3)  # segundos entre solicitudes

    @task(2)
    def list_products(self):
        """Listar productos"""
        self.client.get("/api/products")

    @task(1)
    def create_product(self):
        """Crear un producto nuevo"""
        sku = f"SKU-{random.randint(1000,9999)}"
        data = {
            "name": f"Producto {random.randint(1, 9999)}",
            "sku": sku,
            "description": "Producto de prueba generado automáticamente",
            "quantity": random.randint(1, 100),
            "price": round(random.uniform(10, 500), 2),
            "category": "Pruebas"
        }
        self.client.post("/api/products", json=data)

    @task(1)
    def update_product(self):
        """Actualizar producto existente"""
        product_id = random.randint(1, 10)  # cambia según tus IDs existentes
        data = {
            "name": f"Producto Editado {random.randint(1, 999)}",
            "description": "Actualizado durante prueba de carga",
            "quantity": random.randint(1, 50),
            "price": round(random.uniform(50, 200), 2),
            "category": "Actualizado"
        }
        self.client.put(f"/api/products/{product_id}", json=data)

    @task(1)
    def delete_product(self):
        """Eliminar producto aleatorio (si existe)"""
        product_id = random.randint(1, 10)
        self.client.delete(f"/api/products/{product_id}")
