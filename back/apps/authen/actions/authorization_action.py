from django.contrib.auth import authenticate, login

from apps.authen.processes.authenticate import AuthBackend
from apps.commons.consts.journals.journal_event_results import ERROR, SUCCESS
from apps.commons.consts.journals.journal_rec_types import AUTHEN
from apps.commons.utils.data_types.dict import DictUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.data_types.list import ListUtils
from apps.authen.utils.profile import ProfileUtils
from apps.commons.utils.token import TokenUtils
from apps.journals.writer.journal_writer import JournalWriter


class AuthorizationAction:
    """Класс авторизационных действий"""

    params = ['username', 'password']

    def __init__(self, request, data=None):
        """Инициализация класса - установка полученных имени пользователя и пароля"""
        if data is None:
            self.data = {}

        self.journal = JournalWriter(AUTHEN)
        self.error = ''
        self.data = data
        self.request = request
        self.username = None
        self.password = None

    @property
    def is_request_auth(self) -> bool:
        """Проверка на авторизацию поступившего запроса"""
        auth = AuthBackend()
        __user = auth.authenticate(self.request)
        return __user is not None

    @property
    def is_request_admin(self) -> bool:
        """Проверка на администратора системы"""
        auth = AuthBackend()
        user = auth.authenticate(self.request)
        if user[0] is not None:
            return user[0].is_superuser
        else:
            return False

    def _validate_and_set_data(self):
        """Валидация и установка полученных данных"""
        if (not DictUtils.dict_is_empty(self.data) and
                ListUtils.is_dict_keys_valid_list(self.data, self.params)):
            for key, value in self.data.items():
                setattr(self, key, value)
            return True
        else:
            self.journal.write(
                'Система',
                ERROR,
                f'Произошла ошибка при регистрации пользователя: полученные данные не прошли валидацию'
            )
            return False

    def authorization_user(self) -> dict:
        """Авторизация пользователя"""
        if not self._validate_and_set_data():
            return {'error': 'полученные данные не прошли валидацию'}
        self.error = ''
        pu = ProfileUtils()
        try:
            username = pu.get_username('phone', self.username)
            if username is None:
                username = pu.get_username('email', self.username)
            user = authenticate(
                self.request,
                username=username,
                password=self.password
            )
            if user is not None:
                login(self.request, user)
                auth_data = TokenUtils(user.id).jwt_token()
                self.journal.write(
                    f'{pu.get_display_name('django_user_id', user.id)}',
                    SUCCESS,
                    'Пользователь успешно авторизовался'
                )
                return {
                    'iohk_token': auth_data['access_token'],
                    'iohk_user_id': user.id
                }
            else:
                self.error = 'Неправильный логин или пароль. Повторите попытку'
                self.journal.write('Система', ERROR, self.error)
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Произошла ошибка при авторизации пользователя {self.username}: '
                f'{ExceptionHandling.get_traceback()}'
            )
            self.error = 'Произошла системная ошибка. Повторите попытку позже'
        return {
            'error': self.error
        }
