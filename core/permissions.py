from rest_framework import permissions
from .models import Permission


class RBCPermission(permissions.BasePermission):
    """
    Role Based Access Control Permission.
    """

    def has_permission(self, request, view):
        # 1. Базовая проверка аутентификации
        if not request.user or not request.is_authenticated or not hasattr(request.user, 'role'):
            return False

        # 2. Определяем ресурс
        resource_code = getattr(view, 'resource_code', None)
        if not resource_code:
            return False

            # 3. Ищем права в БД
        try:
            perm = Permission.objects.get(role=request.user.role, resource__code=resource_code)
        except Permission.DoesNotExist:
            return False

            # 4. Проверяем метод
        method = request.method

        if method == 'POST':
            return perm.can_create

        if method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            if perm.can_read_all:
                request.access_scope = 'ALL'
                return True
            if perm.can_read_own:
                request.access_scope = 'OWN'
                return True
            return False

        if method in ['PUT', 'PATCH']:
            if perm.can_update_all:
                request.access_scope = 'ALL'
                return True
            if perm.can_update_own:
                request.access_scope = 'OWN'
                return True
            return False

        if method == 'DELETE':
            if perm.can_delete_all:
                request.access_scope = 'ALL'
                return True
            if perm.can_delete_own:
                request.access_scope = 'OWN'
                return True
            return False

        return False

    def has_object_permission(self, request, view, obj):
        scope = getattr(request, 'access_scope', None)

        if scope == 'ALL':
            return True
        if scope == 'OWN':
            return getattr(obj, 'owner', None) == request.user

        return False