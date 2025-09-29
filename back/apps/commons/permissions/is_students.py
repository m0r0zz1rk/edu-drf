from rest_framework import permissions

from apps.authen.selectors.user import user_orm
from apps.commons.api_exception import GenericAPIException


class IsStudent(permissions.BasePermission):
    """Доступ только для обучающихся в АИС"""
    def has_permission(self, request, view):
        user = user_orm.get_one_record_or_none(filter_by={'id': request.user.id})
        if not user or not user.groups.filter(name='Обучающиеся').exists():
            raise GenericAPIException(detail="Доступ запрещен", status_code=403)
        return True
