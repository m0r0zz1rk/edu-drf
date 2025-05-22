from rest_framework.permissions import IsAuthenticated

from apps.commons.drf.viewset.base_viewset import BaseViewSet
from apps.commons.permissions.is_admin_or_coko import IsAdminOrCoko
from apps.journal.consts.journal_modules import USERS


class UsersViewSet(BaseViewSet):
    """
    Класс вьюсета для пользователей
    """
    permission_classes = [IsAuthenticated, IsAdminOrCoko]
    module = USERS
