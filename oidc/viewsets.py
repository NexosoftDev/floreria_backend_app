from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import json
import base64
from typing import Dict, Any

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User
from oidc.serializers import UserSerializer

"""
VISTAS PARA LA OBTENER LOS USUARIOS QUE EXISTEN EN EL ENDPOINT -> /rest/v1/oidc/obtener-token/ ESTO NOS TRAE TODOS LOS
USUARIOS QUE TENEMOS EN LA BASE DE DATOS, PERO SI QUEREMOS SABER EL TOKEN QUE VIENE DESDE KEYCLOAK PARA EL AUTH,
DEBEMOS DE ENTRAR AL SIGUIENTE ENDPOINT -> rest/v1/oidc/obtener-token/get-token/ ESTO NOS RETORNARA EL TOKEN QUE NOS 
DEVUELVA KEYCLOAK PARA EL INICIO DE SESION USANDO OAUTH V2, Y PARA TRAER LA INFORMACION DEL USUARIO EN SESION LO QUE 
DEBEMOS DE HACER ES INGRESAR AL ENDPOINT -> rest/v1/oidc/obtener-token/me/ ESTO NOS TRAERA LA INFORMACION DEL USUARIO
EN SESIÓN COMO SU USERNAME, CORREO, ETC.
"""

# === Helpers para decodificar JWT y formatear tiempos ===

TZ_LOCAL = ZoneInfo("America/Monterrey")

class OidcViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='get-token', url_name='get-token')
    def get_token(self, request):
        """
        Endpoint para obtener el token OIDC de la sesión actual + expiraciones.
        No requiere autenticación ya que usa la sesión de Django.
        """
        sess = request.session

        access_token = sess.get('oidc_access_token')

        now_local = datetime.now(TZ_LOCAL)

        # Expiración de la sesión de Django
        session_expires_at = sess.get_expiry_date().astimezone(TZ_LOCAL).isoformat()

        data = {
            "now_local": now_local.isoformat(),
            "session": session_expires_at,
            "access_token": access_token,
        }

        if access_token:
            return Response(data)

        return Response({
            "error": "No token found in session",
            "debug": data
        }, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def me(self, request):
        """
        Endpoint para obtener los datos del usuario actual.
        """
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='auth-data', url_name='auth-data')
    def auth_data(self, request):
        """
        Endpoint unificado que devuelve token + datos del usuario.
        Útil para que el frontend obtenga toda la información de autenticación.
        """
        sess = request.session
        access_token = sess.get('oidc_access_token')
        
        if not access_token or not request.user.is_authenticated:
            return Response({
                "error": "No hay sesión activa o token no encontrado",
                "is_authenticated": False
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Datos del usuario
        user_serializer = self.get_serializer(request.user)
        
        # Información de expiración
        now_local = datetime.now(TZ_LOCAL)
        session_expires_at = sess.get_expiry_date().astimezone(TZ_LOCAL).isoformat()
        
        # Decodificar payload del JWT para obtener más info
        jwt_payload = _jwt_payload(access_token)
        token_expires_at = None
        if jwt_payload.get('exp'):
            token_expires_at = _to_local(jwt_payload['exp']).isoformat()

        return Response({
            "is_authenticated": True,
            "access_token": access_token,
            "user": user_serializer.data,
            "session": {
                "expires_at": session_expires_at,
                "current_time": now_local.isoformat()
            },
            "token": {
                "expires_at": token_expires_at,
                "payload": jwt_payload
            }
        })
