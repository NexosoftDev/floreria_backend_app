from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import sys


def health_check(request):
    """
    Health check endpoint para Kubernetes liveness probe
    Verifica que la aplicación está funcionando
    """
    try:
        # Verificar conexión a base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse({
            'status': 'healthy',
            'service': 'floreria-backend',
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        }, status=200)

    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)


def readiness_check(request):
    """
    Readiness check endpoint para Kubernetes readiness probe
    Verifica que la aplicación está lista para recibir tráfico
    """
    try:
        # Verificar base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        # Aquí puedes añadir más verificaciones:
        # - Redis está accesible
        # - Servicios externos responden
        # - Migraciones aplicadas

        return JsonResponse({
            'status': 'ready',
            'service': 'floreria-backend',
            'debug': settings.DEBUG,
        }, status=200)

    except Exception as e:
        return JsonResponse({
            'status': 'not_ready',
            'error': str(e)
        }, status=503)