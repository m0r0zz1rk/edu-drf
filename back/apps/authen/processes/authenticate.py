from datetime import datetime
from typing import Optional

import jwt
from django.contrib.auth.models import User
from rest_framework import authentication

from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import AUTHEN
from apps.commons.utils.django.django import DjangoUtils
from apps.journals.writer.journal_writer import JournalWriter


class AuthenticateCredential:
    """Класс получения данных при аутентификации по JWT токену"""

    journal = JournalWriter(AUTHEN)
    _token = None

    def __init__(self, token):
        """
            Инициализация класса - установка полученного значения токена, создание сущности записи сообщений
            в журнал системных событий
        """
        self.du = DjangoUtils()
        self._token = token

    def validate_and_check_token(self) -> bool:
        """Валидация и проверка полученного токена"""
        try:
            payload = jwt.decode(
                self._token,
                self.du.get_parameter_from_settings('SECRET_KEY'),
                algorithms=self.du.get_parameter_from_settings('JWT_ALGORITHM')
            )
        except jwt.PyJWTError:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при попытке декодирования полученного токена: {self._token}'
            )
            return False

        token_expire = datetime.fromtimestamp(payload['exp'])
        if token_expire < datetime.utcnow():
            self.journal.write(
                'Система',
                ERROR,
                f'Время жизни токена "{self._token}" истекло'
            )
            return False
        return True

    def authenticate_credential(self):
        """Получение пользователя Django на основе токена"""
        if self.validate_and_check_token():
            payload = jwt.decode(self._token,
                                 self.du.get_parameter_from_settings('SECRET_KEY'),
                                 algorithms=self.du.get_parameter_from_settings('JWT_ALGORITHM'))
            if User.objects.filter(id=payload['user_id']).exists():
                user = User.objects.get(id=payload['user_id'])
                return user, None
            else:
                self.journal.write(
                    'Система',
                    ERROR,
                    f'Пользователь по предоставленному токену "{self._token}" не найден'
                )
        return None


class AuthBackend(authentication.BaseAuthentication):
    """Аутентификация на основе JWT токена"""

    journal = JournalWriter(AUTHEN)

    def _validate_header(self, header: list) -> bool:
        """Валидация полученного заголовка запроса"""

        if not header or header[0].lower() != b'token':
            self.journal.write(
                'Система',
                ERROR,
                'Заголовок не содержит данных токена'
            )
            return False

        if len(header) == 1:
            self.journal.write(
                'Система',
                ERROR,
                'Передан некорректный токен в заголовке - отсутствуют авторизационные данные'
            )
            return False
        elif len(header) > 2:
            self.journal.write(
                'Система',
                ERROR,
                'Передан некорректный токен в заголовке - некорректный формат данных'
            )
            return False
        else:
            return True

    def authenticate(self, request, token=None, **kwargs) -> Optional[User]:
        """Валидация заголовка запроса и аутентификация"""
        auth_header = authentication.get_authorization_header(request).split()

        if not self._validate_header(auth_header):
            return None

        try:
            token = auth_header[1].decode('utf-8')
            return AuthenticateCredential(token).authenticate_credential()
        except UnicodeError:
            self.journal.write(
                'Система',
                ERROR,
                f'Ошибка при декодировании токена "{auth_header[1]}" в UTF-8. Токен содержит недопустимые символы'
            )
            return None
