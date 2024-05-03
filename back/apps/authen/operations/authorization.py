from typing import Union

from django.contrib.auth import authenticate, login

from apps.authen.utils.profile import ProfileUtils
from apps.commons.abc.main_processing import MainProcessing
from apps.commons.utils.django.user import UserUtils
from apps.commons.utils.token import TokenUtils
from apps.commons.utils.validate import ValidateUtils
from apps.journal.consts.journal_modules import AUTHEN
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.utils.journal_utils import JournalUtils


class Authorization(MainProcessing):
    """Процесс авторизации пользователей в АИС"""

    required_auth_keys = [
        'request',
        'login',
        'password',
        'centre_auth'
    ]
    ju = JournalUtils()
    uu = UserUtils()
    request = username = password = auth_error = auth_user = auth_data = None

    def _validate_process_data(self) -> Union[bool, str]:
        return ValidateUtils.validate_data(
                self.required_auth_keys,
                self.process_data
        )

    def _auth_error(self, error_type: bool):
        """
        Фиксация ошибки "Пользователь не найден" в журнале обработки
        :param error_type: false - пользователь не найден, true - неверный пароль
        :return:
        """
        journal_payload = {
            'login': self.process_data['login'],
            'password': self.process_data['password'],
        }
        description = 'Пользователь не найден'
        if error_type:
            description = 'Неверный пароль'
        self.ju.create_journal_rec(
            {
                'source': 'Авторизация пользователя',
                'module': AUTHEN,
                'status': ERROR,
                'description': description
            },
            repr(journal_payload),
            None
        )

    def _process_success(self):
        journal_payload = {
            'login': self.process_data['login'],
            'password': self.process_data['password'],
        }
        self.ju.create_journal_rec(
            {
                'source': ProfileUtils().get_profile_or_info_by_attribute(
                    'django_user_id',
                    self.auth_user.id,
                    'display_name'
                ),
                'module': AUTHEN,
                'status': SUCCESS,
                'description': 'Пользователь успешно авторизовался'
            },
            repr(journal_payload),
            None
        )

    def _main_process(self):
        pu = ProfileUtils()
        username = pu.get_profile_or_info_by_attribute(
            'phone',
            self.process_data['login'],
            'username'
        )
        if username is None:
            username = self.uu.get_username_by_email(self.process_data['login'])
            if username is None:
                self.auth_error = 'Пользователь не найден'
                self._auth_error(False)
                self.process_completed = False
                return None
        self.auth_user = authenticate(
            self.process_data['request'],
            username=username,
            password=self.password
        )
        if self.auth_user is None:
            self.auth_error = 'Неверный пароль, повторите попытку'
            self._auth_error(True)
            self.process_completed = False
        login(self.process_data['request'], self.auth_user)
        if self.process_data['centre_auth']:
            if self.request.user.is_staff:
                if self.request.user.is_superuser:
                    self.uu.add_user_to_group('username', username, 'Администраторы')
                else:
                    self.uu.add_user_to_group('username', username, 'Сотрудники')
        self.auth_data = TokenUtils(self.auth_user.id).jwt_token()
