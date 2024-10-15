from django.contrib.auth.models import User
from rest_framework import permissions

from apps.commons.api_exception import GenericAPIException


class IsAdminOrStudent(permissions.BasePermission):
    """Доступ для администраторов или обучающихся АИС"""
    def has_permission(self, request, view):
        if not User.objects.get(id=request.user.id).groups.filter(
                name__in=['Администраторы', 'Обучающиеся']
        ).exists():
            raise GenericAPIException(detail="Доступ запрещен", status_code=403)
        return True
