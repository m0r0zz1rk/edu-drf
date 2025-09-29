from typing import Union

from django.db import transaction

from apps.authen.services.profile import ProfileService
from apps.commons.abc.main_processing import MainProcessing
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.group import GroupUtils
from apps.commons.utils.django.user import UserUtils
from apps.commons.utils.validate import ValidateUtils
from apps.journal.consts.journal_modules import AUTHEN
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.services.journal import journal_service


class Registration(MainProcessing):
    """Процесс регистрации нового пользователя АИС"""

    required_registration_keys = [
        'surname',
        'name',
        'patronymic',
        'phone',
        'email',
        'snils',
        'state',
        'birthday',
        'sex',
        'health',
        'password'
    ]
    pu = ProfileService()
    gu = GroupUtils()
    uu = UserUtils()
    reg_error = None
    username = ''

    def _validate_process_data(self) -> Union[bool, str]:
        return ValidateUtils.validate_data(
            self.required_registration_keys,
            self.process_data
        )

    def _journal_reg_error(self, description: str, output: str = None):
        """
        Фиксация ошибок, возникающих в подпроцессах генерации имени пользователя,
        создании пользователя и его профиля
        :return:
        """
        journal_service.create_journal_rec(
            {
                'source': 'Регистрация нового пользователя',
                'module': AUTHEN,
                'status': ERROR,
                'description': description
            },
            self.process_data,
            output
        )

    def _generate_new_username(self) -> bool:
        """
        Генерация нового имени пользователя
        :return: true - успешно, false - ошибка
        """
        try:
            self.username = self.uu.generate_username(
                self.process_data['surname'],
                self.process_data['name'],
                self.process_data['patronymic'],
            )
            return True
        except Exception:
            self._journal_reg_error('Ошибка при генерации имени пользователя')
            self.reg_error = 'Произошла ошибка при генерации имени пользователя'
            return False

    def _create_user(self) -> bool:
        """Создание нового пользователя"""
        if self.uu.is_user_exists('email', self.process_data['email']):
            self._journal_reg_error('Пользователь с полученным email уже существует')
            self.reg_error = 'Пользователь с полученным email уже существует'
            return False
        try:
            with transaction.atomic():
                if not self._generate_new_username():
                    return False
                create_process = self.uu.create_new_user({
                    'email': self.process_data['email'],
                    'username': self.username,
                    'password': self.process_data['password']
                })
                if create_process is not True:
                    if isinstance(create_process, str):
                        self._journal_reg_error('Системная ошибка', create_process)
                        self.reg_error = create_process
                    else:
                        self._journal_reg_error('Полученные данные о пользователе не прошли валидацию')
                        self.reg_error = 'Полученные данные о пользователе не прошли валидацию'
                    return False
                self.gu.create_group('Обучающиеся')
                self.gu.get_group_by_name('Обучающиеся').user_set.add(
                    self.uu.get_user('email', self.process_data['email'])
                )
                return True
        except Exception:
            self._journal_reg_error('Системная ошибка при создании пользователя', ExceptionHandling.get_traceback())
            self.reg_error = 'Произошла системная ошибка, обратитесь к администратору'
            return False

    def _set_profile_data(self) -> bool:
        """Запись данных в профиль пользователя"""
        if self.pu.is_profile_exist('phone', self.process_data['phone']):
            self._journal_reg_error('Пользователь с таким номером уже существует')
            self.reg_error = 'Пользователь с таким номером телефона уже зарегистрирован'
            return False
        try:
            with transaction.atomic():
                profile_data = {}
                for key, value in self.process_data.items():
                    if key not in ['password', 'email']:
                        profile_data[key] = value
                user_id = self.uu.get_user('email', self.process_data['email']).id
                user_profile = self.pu.get_profile_or_info_by_attribute(
                    'django_user_id',
                    user_id,
                    'profile'
                )
                info_save_process = self.pu.set_student_profile_data(user_profile, profile_data)
                if info_save_process is not True:
                    if isinstance(info_save_process, str):
                        self._journal_reg_error('Системная ошибка при записи данных в профиль', info_save_process)
                        self.reg_error = 'Произошла системная ошибка, обратитесь к администратору'
                    else:
                        self._journal_reg_error('Данные профиля не прошли валидацию')
                        self.reg_error = 'Полученные данные из формы не прошли валидацию'
                    return False
                return True
        except Exception:
            self._journal_reg_error(
                'Ошибка во время процесса записи данных профиля пользователя',
                ExceptionHandling.get_traceback()
            )
            self.reg_error = 'Произошла системная ошибка, обратитесь к администратору'
            return False

    def _main_process(self):
        if self._create_user():
            if self._set_profile_data():
                self.process_completed = True
                return None
        self.process_completed = False

    def _process_success(self):
        journal_service.create_journal_rec(
            {
                'source': 'Регистрация нового пользователя',
                'module': AUTHEN,
                'status': SUCCESS,
                'description': 'Пользователь успешно зарегистрировался'
            },
            self.process_data
        )
