from rest_framework import permissions

from apps.commons.api_exception import GenericAPIException


class IsAuth(permissions.BasePermission):
    """Доступ только для авторизованных пользователей"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise GenericAPIException(detail="Пользователь не авторизован", status_code=401)
        return True
