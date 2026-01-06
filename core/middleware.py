import jwt
from django.conf import settings
from django.http import JsonResponse
from .models import User


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')

        # Сброс пользователя (на всякий случай)
        request.user = None
        request.is_authenticated = False

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = User.objects.get(id=payload['user_id'])

                if user.is_active:
                    request.user = user
                    request.is_authenticated = True
                    # Фикс для совместимости с некоторыми частями Django/DRF
                    request.user.is_authenticated = True

            except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
                # Если токен невалиден, мы можем либо вернуть 401 сразу,
                # либо позволить запросу пройти как "Аноним" (зависит от логики).
                # Здесь оставим проход дальше, права проверит Permission класс.
                pass

        return self.get_response(request)