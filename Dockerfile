# Dockerfile
# Imagen base oficial de Python 3.11 (puedes cambiar a 3.9+ según necesidad)
FROM python:3.11-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero requirements para aprovechar la cache de Docker
COPY requirements.txt ./

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Exponemos el puerto 5000 (el de Flask/gunicorn dentro del contenedor)
EXPOSE 5000

# Comando por defecto: gunicorn para producción
# Puedes modificar WORKERS con una variable de entorno
CMD ["sh", "-c", "gunicorn -w ${WORKERS:-2} -b 0.0.0.0:5000 app:application"]  # 'application' es la instancia creada en app.py
