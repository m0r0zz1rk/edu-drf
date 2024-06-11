from datetime import datetime
from typing import Optional

import jwt

from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.settings import SettingsUtils
from apps.commons.utils.django.user import UserUtils
from apps.journal.consts.journal_modules import AUTHEN
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class JWTCredential:
    """Класс получения данных при аутентификации по JWT токену"""

    _token = None
    payload = None

    def __init__(self, token):
        """
            Инициализация класса - установка полученного значения токена, создание сущности записи сообщений
            в журнал системных событий
        """
        self.du = SettingsUtils()
        self.ju = JournalService()
        self._token = token

    def _journal_error(self, description: str, output: str = None):
        """
        Фиксация ошибок
        :param description: краткое описание ошибки
        :param output: выходные данные (при наличии)
        :return:
        """
        self.ju.create_journal_rec(
            {
                'source': 'Получение данных по JWT токену',
                'module': AUTHEN,
                'status': ERROR,
                'description': description
            },
            self._token,
            output
        )

    def _validate_and_check_token(self) -> bool:
        """
        Валидация и проверка полученного токена
        :return: True - токен верный и валидный, False - проблемы с токеном
        """
        try:
            self.payload = jwt.decode(
                self._token,
                self.du.get_parameter_from_settings('SECRET_KEY'),
                algorithms=self.du.get_parameter_from_settings('JWT_ALGORITHM')
            )
        except jwt.PyJWTError:
            self._journal_error(
                'Ошибка при попытке декодирования полученного токена',
                ExceptionHandling.get_traceback()
            )
            return False
        token_expire = datetime.fromtimestamp(self.payload['exp'])
        if token_expire < datetime.utcnow():
            self._journal_error(
                'Время жизни токена истекло'
            )
            return False
        return True

    def authenticate_credential(self) -> Optional[tuple]:
        """Получение пользователя Django на основе токена"""
        if self._validate_and_check_token():
            user = UserUtils().get_user('id', self.payload['user_id'])
            if user is not None:
                return user, None
            else:
                self._journal_error(
                    'Пользователь не найден'
                )
        return None
