from rest_framework import permissions

from apps.authen.selectors.user import user_orm
from apps.commons.api_exception import GenericAPIException


class IsAdminOrCoko(permissions.BasePermission):
    """Доступ для администраторов или сотрудников ЦОКО в АИС"""
    def has_permission(self, request, view):
        user = user_orm.get_one_record_or_none(filter_by={'id': request.user.id})
        if user and not user.groups.filter(name__in=['Администраторы', 'Сотрудники']).exists():
            raise GenericAPIException(detail="Доступ запрещен", status_code=403)
        return True
