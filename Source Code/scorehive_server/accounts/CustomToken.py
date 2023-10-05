import jwt
from django.conf import settings
from dotenv import load_dotenv
from jwt.exceptions import ExpiredSignatureError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

load_dotenv()


class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request):
        user = None
        try:
            user = super().authenticate(request)
            return user
        except Exception:
            token = self.get_header_token(request)
            if token:
                try:
                    jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
                except ExpiredSignatureError:
                    raise AuthenticationFailed("The token used is expired")
                except Exception:
                    raise AuthenticationFailed("The token used is invalid")
                else:
                    raise AuthenticationFailed("The token used is invalid")
            else:
                raise AuthenticationFailed("Authentication Token not provided")

    def get_header_token(self, request):
        header = self.get_header(request)
        if header is None:
            return None
        return header[7:]
