from typing import Optional

from django.contrib.auth.models import User
from rest_framework import authentication

from apps.commons.utils.django.auth.jwt_credential import JWTCredential
from apps.commons.utils.django.exception import ExceptionHandling
from apps.journal.consts.journal_modules import AUTHEN
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.utils.journal_utils import JournalUtils


class AuthBackend(authentication.BaseAuthentication):
    """Аутентификация на основе JWT токена"""

    ju = JournalUtils()
    auth_header = None

    def _journal_error(self, description: str, payload: str = None, output: str = None):
        """
        Фиксация ошибок
        :param description: краткое описание ошибки
        :param output: выходные данные (при наличии)
        :return:
        """
        self.ju.create_journal_rec(
            {
                'source': 'Аутентификация по JWT токену',
                'module': AUTHEN,
                'status': ERROR,
                'description': description
            },
            payload,
            output
        )

    def _validate_header(self, header: list) -> bool:
        """Валидация полученного заголовка запроса"""
        if not header or header[0].lower() != b'token':
            self._journal_error(
                'Заголовок не содержит данных токена',
                str(self.auth_header)
            )
            return False
        if len(header) == 1:
            self._journal_error(
                'Отсутствует данные авторизации в полученном заголовке',
                str(self.auth_header)
            )
            return False
        elif len(header) > 2:
            self._journal_error(
                'Некорретный формат данных заголовка токена',
                str(self.auth_header)
            )
            return False
        else:
            return True

    def authenticate(self, request, token=None, **kwargs) -> Optional[User]:
        """Валидация заголовка запроса и аутентификация"""
        self.auth_header = authentication.get_authorization_header(request)
        if not self._validate_header(self.auth_header.split()):
            return None
        try:
            token = self.auth_header[1].decode('utf-8')
            return JWTCredential(token).authenticate_credential()
        except UnicodeError:
            self._journal_error(
                'Ошибка при декодировании токена',
                self.auth_header[1],
                ExceptionHandling.get_traceback()
            )
            return None
