from rest_framework.authentication import BaseAuthentication


class MiddlewareAuthentication(BaseAuthentication):
    """
    Простой мост, который говорит DRF:
    'Если Middleware уже нашло юзера, то используй его'.
    """

    def authenticate(self, request):
        # request._request — это "сырой" запрос Django, в котором поработало Middleware
        user = getattr(request._request, 'user', None)

        if user and user.is_authenticated:
            return (user, None)  # (User, Auth)

        return None