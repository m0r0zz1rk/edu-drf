from typing import Optional

from django.contrib.auth.models import User
from rest_framework import authentication

from apps.commons.utils.django.auth.jwt_credential import JWTCredential
from apps.commons.utils.django.exception import ExceptionHandling
from apps.journal.consts.journal_modules import AUTHEN
from apps.journal.consts.journal_rec_statuses import ERROR, JOURNAL_REC_STATUSES, WARNING
from apps.journal.services.journal import JournalService


class AuthBackend(authentication.BaseAuthentication):
    """Аутентификация на основе JWT токена"""

    ju = JournalService()
    auth_header = None

    def _journal_rec(
            self,
            rec_type: JOURNAL_REC_STATUSES,
            description: str,
            payload: str = None,
            output: str = None):
        """
        Фиксация ошибок
        :param rec_type: Тип сообщения
        :param description: краткое описание ошибки
        :param output: выходные данные (при наличии)
        :return:
        """
        self.ju.create_journal_rec(
            {
                'source': 'Аутентификация по JWT токену',
                'module': AUTHEN,
                'status': rec_type,
                'description': description
            },
            payload,
            output
        )

    def _validate_header(self, header: list) -> bool:
        """Валидация полученного заголовка запроса"""
        if not header or header[0].lower() != b'token':
            self._journal_rec(
                WARNING,
                'Заголовок не содержит данных токена',
                str(self.auth_header)
            )
            return False
        if len(header) == 1:
            self._journal_rec(
                ERROR,
                'Отсутствует данные авторизации в полученном заголовке',
                str(self.auth_header)
            )
            return False
        elif len(header) > 2:
            self._journal_rec(
                ERROR,
                'Некорретный формат данных заголовка токена',
                str(self.auth_header)
            )
            return False
        else:
            return True

    def authenticate(self, request, token=None, **kwargs) -> Optional[User]:
        """Валидация заголовка запроса и аутентификация"""
        self.auth_header = authentication.get_authorization_header(request).split()
        if not self._validate_header(self.auth_header):
            return None
        try:
            token = self.auth_header[1].decode('utf-8')
            return JWTCredential(token).authenticate_credential()
        except Exception:
            self._journal_rec(
                ERROR,
                'Ошибка при декодировании токена',
                self.auth_header[1],
                ExceptionHandling.get_traceback()
            )
            return None
