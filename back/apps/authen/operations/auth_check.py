from typing import Optional

from apps.commons.utils.django.auth.auth_backend import AuthBackend
from apps.commons.utils.django.user import UserUtils


class AuthCheck:
    """Проверка запроса пользователя на пройденную авторизацию и функции администраторов или сотрудников"""

    request = None
    __user = None
    uu = UserUtils()
    auth_backend = AuthBackend()

    def __init__(self, request):
        """
        Инициализация класса - установка полученного объекта request
        :return:
        """
        self.request = request
        self.__user = self.auth_backend.authenticate(self.request)

    @property
    def is_request_auth(self) -> bool:
        """Является ли пользователь авторизованным в АИС"""
        return self.__user is not None

    @property
    def get_user_role(self) -> Optional[str]:
        """
        Получение роли пользователя
        :return: str - роль пользователя (centre, dep, student), None - пользователь не авторизован
        """
        if self.__user is None:
            return None
        if self.uu.is_user_in_group('username', self.__user.username, 'Администраторы'):
            return 'centre'
        if self.uu.is_user_in_group('username', self.__user.username, 'Сотрудники'):
            return 'dep'
        return 'student'
