# perfiles/backends.py
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth import get_user_model
from django.conf import settings
import logging
import time

logger = logging.getLogger(__name__)
User = get_user_model()


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):

    def get_token(self, token_payload):
        """Override para agregar logging y medir tiempo"""
        start = time.time()
        logger.info(f"🔄 Iniciando get_token...")
        try:
            result = super().get_token(token_payload)
            elapsed = time.time() - start
            logger.info(f"✅ get_token completado en {elapsed:.2f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"❌ get_token falló después de {elapsed:.2f}s: {e}")
            raise

    def verify_token(self, token, **kwargs):
        """Override para agregar logging, medir tiempo y opcionalmente deshabilitar verificación"""
        start = time.time()

        # Verificar si la verificación de JWT está habilitada
        verify_jwt = getattr(settings, 'OIDC_VERIFY_JWT', True)

        if not verify_jwt:
            logger.warning("⚠️ VERIFICACIÓN DE JWT DESHABILITADA (solo desarrollo)")
            # Decodificar sin verificar
            import json
            import base64
            # Los JWT tienen 3 partes separadas por puntos: header.payload.signature
            parts = token.split('.')
            if len(parts) == 3:
                # Decodificar el payload (segunda parte)
                # Agregar padding si es necesario
                payload = parts[1]
                payload += '=' * (4 - len(payload) % 4)
                decoded = base64.urlsafe_b64decode(payload)
                elapsed = time.time() - start
                logger.info(f"✅ verify_token (sin verificar) completado en {elapsed:.2f}s")
                return json.loads(decoded)
            else:
                raise ValueError("Token JWT inválido")

        logger.info(f"🔄 Iniciando verify_token (con verificación)...")
        try:
            result = super().verify_token(token, **kwargs)
            elapsed = time.time() - start
            logger.info(f"✅ verify_token completado en {elapsed:.2f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"❌ verify_token falló después de {elapsed:.2f}s: {e}")
            raise

    def retrieve_matching_jwk(self, token):
        """Override para cachear JWKS y agregar logging"""
        from django.core.cache import cache

        start = time.time()
        logger.info(f"🔄 Iniciando retrieve_matching_jwk...")

        # Intentar obtener las JWKS del caché
        cache_key = f"oidc_jwks_{settings.OIDC_RP_CLIENT_ID}"
        cached_jwks = cache.get(cache_key)

        if cached_jwks:
            logger.info(f"✅ JWKS obtenidas del caché")
            elapsed = time.time() - start
            logger.info(f"✅ retrieve_matching_jwk completado en {elapsed:.2f}s (desde caché)")
            return cached_jwks

        try:
            result = super().retrieve_matching_jwk(token)
            elapsed = time.time() - start

            # Cachear el resultado
            expiration = getattr(settings, 'OIDC_JWKS_EXPIRATION_TIME', 3600)
            cache.set(cache_key, result, expiration)
            logger.info(f"✅ JWKS cacheadas por {expiration}s")
            logger.info(f"✅ retrieve_matching_jwk completado en {elapsed:.2f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"❌ retrieve_matching_jwk falló después de {elapsed:.2f}s: {e}")
            raise

    def create_user(self, claims):
        """Crear usuario basado en los claims de OIDC"""
        email = claims.get('email')
        if not email:
            logger.warning("No email in claims, cannot create user")
            return None

        # Generar username desde el email si no existe
        username = email.split('@')[0]

        logger.info(f"Creating new user with email: {email}")

        # Extraer otros campos que necesites del claim
        user_data = {
            'username': username,
            'first_name': claims.get('given_name', ''),
            'last_name': claims.get('family_name', ''),
            'is_active': True,
        }

        # Remover campos None o vacíos
        user_data = {k: v for k, v in user_data.items() if v is not None}

        # Llamar al manager con email como argumento separado
        user = User.objects.create_user(email=email, **user_data)
        logger.info(f"User created successfully: {user.email}")
        return user

    def update_user(self, user, claims):
        """Actualizar usuario existente con nuevos claims"""
        logger.info(f"Updating user: {user.email}")
        user.first_name = claims.get('given_name', user.first_name)
        user.last_name = claims.get('family_name', user.last_name)
        user.email = claims.get('email', user.email)
        user.save()
        return user

    def filter_users_by_claims(self, claims):
        """Filtrar usuarios por email"""
        email = claims.get('email')
        if not email:
            logger.warning("No email in claims for filtering")
            return self.UserModel.objects.none()

        users = self.UserModel.objects.filter(email__iexact=email)
        logger.debug(f"Found {users.count()} users with email: {email}")
        return users