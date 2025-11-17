# Imagen base
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto donde corre Flask
EXPOSE 8003

# Definir variables de entorno (puedes ajustarlas si lo deseas)
ENV MONGO_URI="mongodb://mongo:27017"
ENV MONGO_DB="inventory_db"
ENV PRODUCTS_URL="http://laravel_crud:80/api"

# Comando para ejecutar la app
CMD ["python", "app.py"]
