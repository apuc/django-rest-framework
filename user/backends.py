import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth import get_user_model


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None

        prefix, token = auth_data.decode('utf-8').split(' ')

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY)
            user = get_user_model()
            user = user.objects.get(username=payload['username'])
            return (user, token)

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid,login')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'Your token is expired,login')

        return super().authenticate(request)
