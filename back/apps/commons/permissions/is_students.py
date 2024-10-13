from django.contrib.auth.models import User
from rest_framework import permissions

from apps.commons.api_exception import GenericAPIException


class IsStudent(permissions.BasePermission):
    """Доступ только для обучающихся в АИС"""
    def has_permission(self, request, view):
        if not User.objects.get(id=request.user.id).groups.filter(name='Обучающиеся').exists():
            raise GenericAPIException(detail="Доступ запрещен", status_code=403)
        return True
