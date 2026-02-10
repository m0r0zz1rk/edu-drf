from copy import copy
from typing import Union

from django.contrib.auth import authenticate, login

from apps.authen.services.profile import ProfileService, profile_service
from apps.commons.abc.main_processing import MainProcessing
from apps.commons.services.ad.ad_centre_coko_user import ad_centre_coko_user_utils
from apps.commons.utils.django.user import user_utils
from apps.commons.utils.ldap import ldap_utils
from apps.commons.utils.token import TokenUtils
from apps.commons.utils.validate import ValidateUtils
from apps.journal.consts.journal_modules import AUTHEN
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.services.journal import journal_service


class Authorization(MainProcessing):
    """Процесс авторизации пользователей в АИС"""

    required_auth_keys = [
        'request',
        'login',
        'password',
        'centre_auth'
    ]
    request = username = auth_error = auth_user = auth_data = None

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
            'password': '*******',
        }
        description = 'Пользователь не найден'
        if error_type:
            description = 'Неверный пароль'
        journal_service.create_journal_rec(
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
            'password': '*******',
        }
        journal_service.create_journal_rec(
            {
                'source': ProfileService().get_profile_or_info_by_attribute(
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
        username = self.process_data.get('login')
        centre_auth = self.process_data.get('centre_auth')
        if not centre_auth:
            user_login = self.process_data.get('login')
            username = profile_service.get_profile_or_info_by_attribute(
                'phone',
                user_login,
                'username'
            )
            if username is None:
                username = profile_service.get_profile_or_info_by_attribute(
                    'snils',
                    user_login,
                    'username'
                )
                if username is None:
                    if '@coko38.ru' in user_login:
                        self.auth_error = 'Для авторизации используйте форму входа на вкладке "Сотрудник центра"'
                        self._auth_error(False)
                        self.process_completed = False
                        return None
                    username = user_utils.get_username_by_email(user_login)
                    if username is None:
                        self.auth_error = 'Пользователь не найден'
                        self._auth_error(False)
                        self.process_completed = False
                        return None
        self.auth_user = authenticate(
            self.process_data['request'],
            username=username,
            password=self.process_data['password']
        )
        if self.auth_user is None:
            self.auth_error = 'Неверный пароль, повторите попытку'
            self._auth_error(True)
            self.process_completed = False
        login(self.process_data['request'], self.auth_user)
        if centre_auth:
            profile = profile_service.get_profile_or_info_by_attribute(
                'django_user_id',
                self.auth_user.id,
                'profile'
            )
            if self.auth_user.is_staff and not self.auth_user.is_superuser:
                centre_info = ldap_utils.get_ad_user_centre(self.auth_user)
                if centre_info:
                    ad_centre_coko_user_utils.add_rec(
                        self.auth_user,
                        centre_info[1]
                    )
            if profile.internal_phone == 100:
                try:
                    profile_service.set_coko_profile_data(
                        profile,
                        {
                            'internal_phone': ldap_utils.get_ad_attribute_coko_user(
                                'telephoneNumber',
                                self.auth_user.username
                            )
                        }
                    )
                except Exception as e:
                    pass
            if profile.surname == 'Фамилия':
                profile_service.set_coko_profile_data(
                    profile,
                    {
                        'surname': ldap_utils.get_ad_attribute_coko_user(
                            'sn',
                            self.auth_user.username
                        ),
                        'name': ldap_utils.get_ad_attribute_coko_user(
                            'GivenName',
                            self.auth_user.username
                        ),
                        'patronymic': ldap_utils.get_ad_attribute_coko_user(
                            'middleName',
                            self.auth_user.username
                        ),
                        'internal_phone': ldap_utils.get_ad_attribute_coko_user(
                            'telephoneNumber',
                            self.auth_user.username
                        )
                    }
                )
                if self.auth_user.is_staff:
                    if self.auth_user.is_superuser:
                        user_utils.add_user_to_group('username', username, 'Администраторы')
                    else:
                        user_utils.add_user_to_group('username', username, 'Сотрудники')
        self.auth_data = TokenUtils(self.auth_user.id).jwt_token()
