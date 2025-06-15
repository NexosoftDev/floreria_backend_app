# Sistema Backend para Floristería

Una aplicación backend completa desarrollada con Django REST Framework para la gestión integral de una floristería. Incluye autenticación con Keycloak, gestión de inventario, procesamiento de pedidos, y un sistema completo de administración para negocios florales.

## Descripción General

Este sistema backend proporciona una solución completa para la gestión de floristerías, integrando todas las funcionalidades necesarias para operar un negocio floral moderno. Desde la gestión de inventario de flores y productos hasta el procesamiento de pedidos y entregas a domicilio.

## Características Principales

- **Autenticación Segura**: Integración completa con Keycloak usando OpenID Connect (OIDC)
- **Gestión de Inventario**: Control total de flores, plantas, y productos complementarios
- **Procesamiento de Pedidos**: Sistema completo de pedidos con estados y seguimiento
- **Gestión de Clientes**: Administración de datos de clientes y historial de compras
- **Sistema de Entregas**: Gestión de entregas a domicilio con seguimiento
- **Reportes y Analytics**: Informes detallados de ventas, inventario y rendimiento
- **API RESTful**: API completa para integración con aplicaciones frontend
- **Panel de Administración**: Interface administrativa para gestión completa del negocio
- **Notificaciones**: Sistema de notificaciones para pedidos y entregas
- **Gestión de Proveedores**: Control de proveedores y compras

## Requisitos Previos

- Python 3.8 o superior
- Django 3.2 o superior
- Django REST Framework 3.12 o superior
- PostgreSQL 12 o superior (recomendado)
- Redis (para caché y tareas asíncronas)
- Acceso a un servidor Keycloak (local o remoto)

## Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/NexosoftDev/floreria_backend_app.git
cd floreria_backend_app
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt

# Instalar dependencias adicionales
pip install mozilla-django-oidc
pip install redis
pip install celery
pip install pillow  # Para manejo de imágenes
```

### 4. Configuración del Entorno

Crea un archivo `.env` en la raíz del proyecto con la siguiente configuración:

```env
# Configuración de Django
DEBUG=True
SECRET_KEY="tu-clave-privada-generada-con-openssl"
SECRET_KEY_LOCAL="tu-secret-key-temporal-para-desarrollo"

# Configuración de Base de Datos
DATABASE_URL="postgresql://usuario:contraseña@localhost:5432/floreria_db"

# Configuración de Keycloak OIDC
OIDC_OP_BASE_URL="https://tu-servidor-keycloak.com/realms/floreria/"
OIDC_RP_CLIENT_ID="floreria-backend"
OIDC_RP_CLIENT_SECRET="tu-client-secret"
LOGOUT_REDIRECT_URL="http://localhost:8000"

# Configuración de Redis
REDIS_URL="redis://localhost:6379/0"
CELERY_BROKER_URL="redis://localhost:6379/0"
CELERY_RESULT_BACKEND="redis://localhost:6379/0"

# Configuración de Email
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER="tu-email@gmail.com"
EMAIL_HOST_PASSWORD="tu-contraseña-de-aplicacion"

# Configuración de Archivos Estáticos
MEDIA_ROOT="/ruta/a/media/"
STATIC_ROOT="/ruta/a/static/"

# Configuración de API Externa (opcional)
MAPS_API_KEY="tu-api-key-de-google-maps"
PAYMENT_GATEWAY_KEY="tu-clave-de-pasarela-de-pago"

# Configuración de Seguridad
ALLOWED_HOSTS="localhost,127.0.0.1,tu-dominio.com"
CORS_ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

### 5. Generación de Claves Seguras

#### Clave de Producción (SECRET_KEY)
```bash
openssl genrsa -out private_key.pem 2048
```

#### Clave de Desarrollo (SECRET_KEY_LOCAL)
```bash
openssl rand -base64 32
```

### 6. Configuración de Base de Datos

```bash
# Crear la base de datos PostgreSQL
createdb floreria_db

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar datos iniciales (opcional)
python manage.py loaddata fixtures/initial_data.json
```

### 7. Configurar Redis y Celery

```bash
# Iniciar Redis (en otra terminal)
redis-server

# Iniciar Celery Worker (en otra terminal)
celery -A floreria_backend worker --loglevel=info

# Iniciar Celery Beat para tareas programadas (en otra terminal)
celery -A floreria_backend beat --loglevel=info
```

### 8. Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en `http://localhost:8000`

## Configuración de Keycloak

### Configuración del Cliente

1. **Acceder a la Consola de Administración de Keycloak**
   - Navegar a la interfaz de administración de Keycloak
   - Seleccionar el realm "floreria"

2. **Crear Cliente OIDC**
   - Ir a Clientes → Crear Cliente
   - Configurar:
     - Client ID: `floreria-backend`
     - Tipo de cliente: "OpenID Connect"
     - Autenticación de cliente: ON

3. **Configurar URIs del Cliente**
   - **URIs de redirección válidas**: `http://localhost:8000/oidc/callback/`
   - **URIs de post-logout válidas**: `http://localhost:8000/`
   - **Orígenes web**: `http://localhost:8000`

### Configuración de Roles y Grupos

Crear los siguientes roles en Keycloak:
- `floreria_admin`: Administrador completo del sistema
- `floreria_manager`: Gerente de floristería
- `floreria_employee`: Empleado de floristería
- `floreria_delivery`: Personal de entrega
- `floreria_customer`: Cliente registrado

## Estructura del Proyecto

```
floreria_backend_app/
├── apps/
│   ├── authentication/      # Autenticación y usuarios
│   ├── inventory/          # Gestión de inventario
│   ├── orders/            # Procesamiento de pedidos
│   ├── customers/         # Gestión de clientes
│   ├── delivery/          # Sistema de entregas
│   ├── products/          # Gestión de productos
│   ├── suppliers/         # Gestión de proveedores
│   ├── reports/           # Reportes y analytics
│   └── notifications/     # Sistema de notificaciones
├── config/
│   ├── settings/          # Configuraciones por entorno
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # Configuración WSGI
├── static/               # Archivos estáticos
├── media/               # Archivos de media
├── templates/           # Plantillas HTML
├── fixtures/            # Datos iniciales
├── requirements.txt     # Dependencias Python
└── manage.py           # Script de gestión Django
```

## Referencia de Variables de Entorno

| Variable | Descripción | Requerida | Ejemplo |
|----------|-------------|-----------|---------|
| `SECRET_KEY` | Clave RSA privada para firma JWT (producción) | Sí | `-----BEGIN RSA PRIVATE KEY-----\n...` |
| `SECRET_KEY_LOCAL` | Clave base64 para desarrollo | Sí | `abc123def456...` |
| `DATABASE_URL` | URL completa de conexión a PostgreSQL | Sí | `postgresql://user:pass@localhost:5432/db` |
| `OIDC_OP_BASE_URL` | URL base del realm de Keycloak | Sí | `https://keycloak.example.com/realms/floreria/` |
| `OIDC_RP_CLIENT_ID` | Identificador del cliente en Keycloak | Sí | `floreria-backend` |
| `OIDC_RP_CLIENT_SECRET` | Secreto del cliente en Keycloak | Sí | `tu-client-secret` |
| `REDIS_URL` | URL de conexión a Redis | Sí | `redis://localhost:6379/0` |
| `EMAIL_HOST` | Servidor SMTP para envío de emails | No | `smtp.gmail.com` |
| `MAPS_API_KEY` | Clave API de Google Maps | No | `AIza...` |

## Endpoints de la API

### Autenticación

| Endpoint | Método | Descripción | Autenticación |
|----------|--------|-------------|---------------|
| `/oidc/authenticate/` | GET | Iniciar flujo de autenticación OIDC | No |
| `/oidc/callback/` | GET/POST | Callback de autenticación OIDC | No |
| `/oidc/logout/` | GET/POST | Cerrar sesión OIDC | Sesión |
| `/api/v1/auth/token/` | POST | Obtener token JWT | Sesión |
| `/api/v1/auth/me/` | GET | Información del usuario actual | Token |

### Productos e Inventario

| Endpoint | Método | Descripción | Autenticación |
|----------|--------|-------------|---------------|
| `/api/v1/products/` | GET/POST | Listar/crear productos | Token |
| `/api/v1/products/{id}/` | GET/PUT/PATCH/DELETE | Gestionar producto específico | Token |
| `/api/v1/inventory/` | GET/POST | Gestión de inventario | Token |
| `/api/v1/inventory/low-stock/` | GET | Productos con stock bajo | Token |
| `/api/v1/categories/` | GET/POST | Gestión de categorías | Token |

### Pedidos

| Endpoint | Método | Descripción | Autenticación |
|----------|--------|-------------|---------------|
| `/api/v1/orders/` | GET/POST | Listar/crear pedidos | Token |
| `/api/v1/orders/{id}/` | GET/PUT/PATCH | Gestionar pedido específico | Token |
| `/api/v1/orders/{id}/status/` | PATCH | Actualizar estado del pedido | Token |
| `/api/v1/orders/today/` | GET | Pedidos del día | Token |
| `/api/v1/orders/pending/` | GET | Pedidos pendientes | Token |

### Clientes

| Endpoint | Método | Descripción | Autenticación |
|----------|--------|-------------|---------------|
| `/api/v1/customers/` | GET/POST | Gestión de clientes | Token |
| `/api/v1/customers/{id}/` | GET/PUT/PATCH/DELETE | Cliente específico | Token |
| `/api/v1/customers/{id}/orders/` | GET | Historial de pedidos del cliente | Token |
| `/api/v1/customers/search/` | GET | Buscar clientes | Token |

### Entregas

| Endpoint | Método | Descripción | Autenticación |
|----------|--------|-------------|---------------|
| `/api/v1/deliveries/` | GET/POST | Gestión de entregas | Token |
| `/api/v1/deliveries/{id}/` | GET/PUT/PATCH | Entrega específica | Token |
| `/api/v1/deliveries/route/` | GET | Optimizar ruta de entregas | Token |
| `/api/v1/deliveries/tracking/{id}/` | GET | Seguimiento de entrega | Token/Público |

### Reportes

| Endpoint | Método | Descripción | Autenticación |
|----------|--------|-------------|---------------|
| `/api/v1/reports/sales/` | GET | Reporte de ventas | Token |
| `/api/v1/reports/inventory/` | GET | Reporte de inventario | Token |
| `/api/v1/reports/customers/` | GET | Reporte de clientes | Token |
| `/api/v1/reports/export/` | GET | Exportar reportes | Token |

## Modelos de Datos Principales

### Producto
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    minimum_stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Pedido
```python
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmado'),
        ('preparing', 'En Preparación'),
        ('ready', 'Listo'),
        ('in_delivery', 'En Entrega'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]
    
    customer = models.ForeignKey(Customer)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateTimeField()
    delivery_address = models.TextField()
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Ejemplos de Uso

### Integración Frontend

```javascript
// Autenticación
const login = () => {
    window.location.href = '/oidc/authenticate/';
};

// Obtener token
const getToken = async () => {
    const response = await fetch('/api/v1/auth/token/', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    });
    const data = await response.json();
    return data.access_token;
};

// Crear pedido
const createOrder = async (orderData, token) => {
    const response = await fetch('/api/v1/orders/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
    });
    return await response.json();
};

// Obtener productos
const getProducts = async (token) => {
    const response = await fetch('/api/v1/products/', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return await response.json();
};
```

### Uso de la API con curl

```bash
# Obtener productos
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/api/v1/products/

# Crear nuevo pedido
curl -X POST \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"customer_id": 1, "products": [{"id": 1, "quantity": 2}]}' \
     http://localhost:8000/api/v1/orders/

# Actualizar estado de pedido
curl -X PATCH \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"status": "confirmed"}' \
     http://localhost:8000/api/v1/orders/1/status/
```

## Configuración de Endpoints OIDC

El sistema configura automáticamente los siguientes endpoints OIDC basados en `OIDC_OP_BASE_URL`:

```python
OIDC_OP_AUTHORIZATION_ENDPOINT = f'{OIDC_OP_BASE_URL}/protocol/openid-connect/auth'
OIDC_OP_TOKEN_ENDPOINT = f'{OIDC_OP_BASE_URL}/protocol/openid-connect/token'
OIDC_OP_USER_ENDPOINT = f'{OIDC_OP_BASE_URL}/protocol/openid-connect/userinfo'
OIDC_OP_JWKS_ENDPOINT = f'{OIDC_OP_BASE_URL}/protocol/openid-connect/certs'
```

## Desarrollo vs Producción

### Entorno de Desarrollo
- Usar `SECRET_KEY_LOCAL` para gestión simplificada de claves
- Configurar `DEBUG=True`
- Usar SQLite para desarrollo rápido (opcional)
- `OIDC_VERIFY_SSL=False` para certificados auto-firmados

### Entorno de Producción
- Usar siempre `SECRET_KEY` segura generada con OpenSSL
- Configurar `DEBUG=False`
- Usar PostgreSQL para mejor rendimiento
- Habilitar verificación SSL (`OIDC_VERIFY_SSL=True`)
- Usar variables de entorno del sistema
- Configurar URIs HTTPS apropiadas
- Implementar monitoreo y logging
- Configurar backup automático de base de datos

## Tareas Asíncronas con Celery

El sistema incluye las siguientes tareas asíncronas:

```python
# Envío de notificaciones
@shared_task
def send_order_notification(order_id):
    # Enviar notificación de pedido

# Actualización de inventario
@shared_task
def update_inventory_levels():
    # Actualizar niveles de inventario

# Generación de reportes
@shared_task
def generate_daily_report():
    # Generar reporte diario
```

## Solución de Problemas

### Problemas Comunes

1. **Error de Autenticación OIDC**
   - Verificar configuración del cliente en Keycloak
   - Confirmar URIs de redirección exactas
   - Validar secreto del cliente

2. **Problemas de Base de Datos**
   - Verificar conexión a PostgreSQL
   - Ejecutar migraciones pendientes
   - Revisar permisos de usuario de BD

3. **Errores de Redis/Celery**
   - Confirmar que Redis esté ejecutándose
   - Verificar configuración de Celery
   - Revisar logs de worker

### Depuración

Habilitar logs detallados:

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'floreria.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
        },
        'floreria_backend': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
        'mozilla_django_oidc': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Consideraciones de Seguridad

- **Nunca commitear secretos**: Mantener archivos `.env` fuera del control de versiones
- **Usar HTTPS**: Siempre usar HTTPS en entornos de producción
- **Seguridad de Tokens**: Implementar rotación apropiada de tokens
- **Actualizaciones Regulares**: Mantener dependencias actualizadas
- **Control de Acceso**: Implementar control de acceso basado en roles
- **Validación de Datos**: Validar todos los datos de entrada
- **Backup de Seguridad**: Implementar backups regulares y seguros

## Contribución

1. Fork del repositorio
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Realizar cambios y commits
4. Agregar tests si es aplicable
5. Enviar pull request

## Soporte

Para problemas y preguntas:
- Revisar la sección de [Issues](https://github.com/NexosoftDev/floreria_backend_app/issues)
- Consultar documentación de Django y Keycloak
- Contactar al equipo de desarrollo

## Licencia
