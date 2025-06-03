from mozilla_django_oidc.views import OIDCAuthenticationCallbackView
from django.shortcuts import redirect


class CustomOIDCCallbackView(OIDCAuthenticationCallbackView):

    def get(self, request):
        print("Entré a CustomOIDCCallbackView")  # <-- Aquí
        response = super().get(request)
        token = request.session.get('oidc_access_token')
        print(token, 'token')
        if token:
            redirect_url = 'http://localhost:3000/?token=' + token
            return redirect(redirect_url)
        else:
            print("No encontré token en sesión")
            return response