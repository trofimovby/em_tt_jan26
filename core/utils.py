import jwt
import datetime
from django.conf import settings


def generate_jwt_token(user_id, role_name):
    """
    Генерирует JWT токен вручную, используя библиотеку pyjwt.
    """
    payload = {
        'user_id': user_id,
        'role': role_name,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),  # Токен живет 24 часа
        'iat': datetime.datetime.utcnow()  # Время создания
    }

    # Используем SECRET_KEY из settings.py для подписи
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token