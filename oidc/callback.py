from mozilla_django_oidc.views import OIDCAuthenticationCallbackView
from django.shortcuts import redirect


class CustomOIDCCallbackView(OIDCAuthenticationCallbackView):

    def get(self, request):

        response = super().get(request)

        if request.session.get('oidc_access_token'):
            return redirect('http://localhost:3000/')
        else:
            print("No encontré token en sesión")
            return response