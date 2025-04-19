from apps.commons.drf.viewset.base_viewset import BaseViewSet
from apps.journal.consts.journal_modules import USERS


class UsersViewSet(BaseViewSet):
    """
    Класс вьюсета для пользователей
    """
    module = USERS
