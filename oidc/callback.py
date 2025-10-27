from mozilla_django_oidc.views import OIDCAuthenticationCallbackView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.cache import cache
from FLORERIA.settings import LOGIN_REDIRECT_URL
from urllib.parse import urlencode
import logging
import time

logger = logging.getLogger(__name__)
class CustomOIDCCallbackView(OIDCAuthenticationCallbackView):
    def get(self, request):
        start_time = time.time()
        logger.info(f"🔵 OIDC Callback iniciado - URL: {request.get_full_path()}")
        logger.info(f"Query params: {request.GET}")
        print("hola")

        try:
            # Llamar al método padre para autenticar
            logger.info("Llamando a super().get() para autenticar...")
            response = super().get(request)
            elapsed = time.time() - start_time
            logger.info(f"⏱️ Autenticación completada en {elapsed:.2f} segundos")

            logger.info(f"Usuario autenticado: {request.user.is_authenticated}")
            logger.info(f"Usuario: {request.user}")

            access_token = request.session.get('oidc_access_token')
            id_token = request.session.get('oidc_id_token')
            logger.info(f"Access token en sesión: {'✓' if access_token else '✗'}")
            logger.info(f"ID token en sesión: {'✓' if id_token else '✗'}")

            if access_token and request.user.is_authenticated:
                logger.info("✅ Autenticación exitosa - Preparando redirección")

                user_data = {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                }

                # Guardar en caché para que el frontend pueda recuperarlo
                cache.set(f"oidc_token_{request.user.email}", access_token, timeout=3600)
                cache.set(f"oidc_user_{request.user.email}", user_data, timeout=3600)
                logger.info(f"Datos guardados en caché para: {request.user.email}")

                frontend_url = LOGIN_REDIRECT_URL
                logger.info(f"Frontend URL: {frontend_url}")

                params = {
                    'token': access_token,
                    **user_data,
                    'is_authenticated': 'true',
                }

                redirect_url = f"{frontend_url}?{urlencode(params)}"
                logger.info(f"🚀 Redirigiendo a: {redirect_url}")

                total_time = time.time() - start_time
                logger.info(f"✅ Callback completado en {total_time:.2f} segundos")

                return HttpResponseRedirect(redirect_url)
            else:
                logger.warning("⚠️ Usuario no autenticado o token ausente después de super().get()")
                logger.warning(f"access_token existe: {bool(access_token)}")
                logger.warning(f"user.is_authenticated: {request.user.is_authenticated}")

                # Intentar devolver la respuesta original si existe
                if response:
                    return response

                return JsonResponse({
                    'status': 'error',
                    'message': 'Autenticación fallida',
                    'details': 'Usuario no autenticado o token ausente'
                }, status=400)

        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"❌ Error en callback después de {elapsed:.2f} segundos: {str(e)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'Error durante la autenticación',
                'details': str(e)
            }, status=500)