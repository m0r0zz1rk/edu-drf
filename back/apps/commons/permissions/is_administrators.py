from rest_framework import permissions

from apps.authen.selectors.user import user_orm
from apps.commons.api_exception import GenericAPIException


class IsAdministrators(permissions.BasePermission):
    """Доступ только для администраторов АИС"""
    def has_permission(self, request, view):
        user = user_orm.get_one_record_or_none(filter_by={'id': request.user.id})
        if not user or not user.groups.filter(name='Администраторы').exists():
            raise GenericAPIException(detail="Доступ запрещен", status_code=403)
        return True
