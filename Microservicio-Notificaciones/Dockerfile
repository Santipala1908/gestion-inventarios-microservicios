# Imagen base ligera de Python
FROM python:3.11-slim

# Evitar .pyc y usar salida sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto interno donde corre Flask
EXPOSE 8005

# Comando para arrancar el microservicio
CMD ["python", "app.py"]
