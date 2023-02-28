from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import authentication
from rest_framework import exceptions


class RequiresSessionAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        if not (request.session and request.session.session_key):
            raise exceptions.AuthenticationFailed("No session key")


class RequiresSessionExtension(OpenApiAuthenticationExtension):
    target_class = "shiritori.game.auth.RequiresSessionAuth"
    name = "RequiresSessionAuth"

    def get_security_definition(self, auto_schema):
        return {"type": "apiKey", "in": "cookie", "name": "sessionid"}
