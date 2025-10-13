# oidc/callback.py
from mozilla_django_oidc.views import OIDCAuthenticationCallbackView
from django.shortcuts import redirect
from django.core.cache import cache
from django.http import HttpResponseRedirect
from FLORERIA.settings import LOGIN_REDIRECT_URL
from urllib.parse import urlencode
import json
import logging

logger = logging.getLogger(__name__)


class CustomOIDCCallbackView(OIDCAuthenticationCallbackView):

    def get(self, request):
        logger.info(f"OIDC Callback iniciado - URL: {request.get_full_path()}")
        logger.info(f"Query params: {request.GET}")
        
        response = super().get(request)
        
        logger.info(f"Usuario autenticado: {request.user.is_authenticated}")
        logger.info(f"Usuario: {request.user}")
        
        access_token = request.session.get('oidc_access_token')
        logger.info(f"Token en sesión: {'Sí' if access_token else 'No'}")
        
        if access_token and request.user.is_authenticated:
            logger.info("✅ Condiciones cumplidas - Procesando redirección con datos")
            
            # Datos del usuario para el frontend
            user_data = {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
            
            logger.info(f"Datos del usuario: {user_data}")
            cache_key = f"oidc_token_{request.user.email}"
            cache.set(cache_key, access_token, timeout=3600)

            user_cache_key = f"oidc_user_{request.user.email}"
            cache.set(user_cache_key, user_data, timeout=3600)


            frontend_url = LOGIN_REDIRECT_URL
            logger.info(f"Frontend URL configurada: {frontend_url}")
            
            params = {
                'token': access_token,
                'user_id': request.user.id,
                'email': request.user.email,
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'is_authenticated': 'true'
            }
            
            redirect_url = f"{frontend_url}?{urlencode(params)}"
            logger.info(f"🚀 Redirigiendo a: {redirect_url}")

            return HttpResponseRedirect(redirect_url)
        else:

            return response