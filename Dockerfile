# Usar imagen base oficial de Python
FROM python:3.11-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para Pillow y cryptography
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

# Copiar el código de la aplicación
COPY . .

# Crear directorio para archivos estáticos y media
RUN mkdir -p /app/staticfiles /app/media

# Exponer el puerto 8000
EXPOSE 8000

# Ejecutar migraciones y collectstatic, luego iniciar gunicorn
 # Ejecutar migraciones y collectstatic, luego iniciar el servidor de desarrollo
CMD bash -c "
    python manage.py makemigrations --noinput &&
    python manage.py migrate --noinput &&
    python manage.py collectstatic --noinput &&
    echo 'from django.contrib.auth.models import User; \
          User.objects.filter(username=\"admin\").exists() or \
          User.objects.create_superuser(\"admin\", \"admin@example.com\", \"admin123\")' \
          | python manage.py shell &&
    python manage.py runserver 0.0.0.0:8000
"
