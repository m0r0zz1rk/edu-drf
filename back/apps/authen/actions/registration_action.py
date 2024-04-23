import datetime

from django.contrib.auth.models import User, Group
from django.db import transaction

from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import AUTHEN
from apps.commons.utils.data_types.dict import DictUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.generate import GenerateUtils
from apps.commons.utils.data_types.list import ListUtils
from apps.authen.utils.profile import ProfileUtils
from apps.journals.writer.journal_writer import JournalWriter


class RegistrationAction:
    """Класс регистрационных действий"""

    params = [
        'state',
        'surname',
        'name',
        'patronymic',
        'sex',
        'birthday',
        'phone',
        'email',
        'role',
        'oo_fullname',
        'oo_shortname',
        'password'
    ]

    def __init__(self, data: dict):
        """Инициализация класса - установка данных по умолчанию """
        self.journal = JournalWriter(AUTHEN)
        self.data = data
        self.django_user_id = 1
        self.username = ''

    def _validate_and_set_data(self):
        """Валидация полученных данных"""
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

    def _generate_new_username(self):
        """Генерация нового имени пользователя"""
        try:
            du = DictUtils()
            gu = GenerateUtils()
            self.username = gu.generate_username(
                du.get_str_value_in_dict_by_key('surname', self.data),
                du.get_str_value_in_dict_by_key('name', self.data),
                du.get_str_value_in_dict_by_key('patronymic', self.data)
            )
            return True
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Произошла ошибка во время генерации имени пользователя при регистрации: '
                f'{ExceptionHandling.get_traceback()}'
            )
            return False

    def _create_user(self) -> bool:
        """Создание нового пользователя"""
        du = DictUtils()
        if ProfileUtils.check_profile_exists(
                'email',
                du.get_str_value_in_dict_by_key('email', self.data)):
            self.journal.write(
                'Система',
                ERROR,
                f'Произошла ошибка при регистрации пользователя: '
                f'"{du.get_str_value_in_dict_by_key('email', self.data)}" уже зарегистрирован'
            )
            return False
        try:
            with transaction.atomic():
                self._generate_new_username()
                new_user = User.objects.create_user(
                    username=self.username,
                    password=du.get_str_value_in_dict_by_key('password', self.data),
                    email=du.get_str_value_in_dict_by_key('email', self.data)
                )
                self.django_user_id = new_user.id
                if du.get_str_value_in_dict_by_key('role', self.data) in ['Участники', 'Преподаватели']:
                    gr = Group.objects.get(name=du.get_str_value_in_dict_by_key('role', self.data))
                else:
                    gr = Group.objects.get(name='Участники')
                gr.user_set.add(new_user)
                return True
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Произошла ошибка во время создания Django User при регистрации пользователя: '
                f'{ExceptionHandling.get_traceback()}'
            )
        return False

    def _create_user_profile(self) -> bool:
        """Создание нового профиля пользователя"""
        du = DictUtils()
        if ProfileUtils.check_profile_exists(
            'phone',
            du.get_str_value_in_dict_by_key('phone', self.data)
        ):
            self.journal.write(
                'Система',
                ERROR,
                f'Произошла ошибка при регистрации пользователя: '
                f'"{du.get_str_value_in_dict_by_key('phone', self.data)}" уже зарегистрирован'
            )
            return False
        try:
            with transaction.atomic():
                delta = datetime.datetime.now() - du.get_date_value_in_dict_by_key('birthday', self.data)
                profile_data = {
                    'age': delta.days // 365
                }
                for key, value in self.data.items():
                    if key not in ['password', 'role']:
                        if key == 'state':
                            profile_data['state_id'] = value
                        elif key == 'birthday':
                            profile_data['birthday'] = du.get_date_value_in_dict_by_key('birthday', self.data)
                        else:
                            profile_data[key] = value
                user_profile = ProfileUtils.get_profile_by_user_id(self.django_user_id)
                for k, v in profile_data.items():
                    setattr(user_profile, k, v)
                user_profile.save()
                return True
        except Exception:
            self.journal.write(
                'Система',
                ERROR,
                f'Произошла ошибка во время создания профиля при регистрации пользователя: '
                f'{ExceptionHandling.get_traceback()}'
            )
        return False

    def registration(self) -> bool:
        """
            Регистрация нового пользователя в системе, создание профиля
        """
        if self._validate_and_set_data():
            try:
                with transaction.atomic():
                    new_user = self._create_user()
                    if new_user is False:
                        return False
                    new_profile = self._create_user_profile()
                    if new_profile is False:
                        User.objects.get(username=self.username).delete()
                        return False
                    return True
            except Exception:
                pass
        return False
