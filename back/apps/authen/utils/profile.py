from typing import Union

from django.apps import apps

from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.user import UserUtils
from apps.commons.utils.validate import ValidateUtils

student_profile_model = apps.get_model('authen', 'StudentProfile')
coko_profile_model = apps.get_model('authen', 'CokoProfile')
state_model = apps.get_model('guides', 'State')

set_student_profile_fields = [
    'surname',
    'name',
    'patronymic',
    'phone',
    'email',
    'snils',
    'state',
    'birthday',
    'sex',
    'health'
]
set_coko_profile_fields = [
    'surname',
    'name',
    'patronymic',
]


class ProfileUtils:
    """Класс методов для работы с профилями пользователей"""

    @staticmethod
    def is_profile_exist(attribute_name: str, value) -> bool:
        """
        Проверка на существующий профиль пользователя по заданному атрибуту и его значению
        :param attribute_name: наименование атрибута (поле модели профиля)
        :param value: значение
        :return: true - профиль существует, false - профиль не существует
        """
        data = {attribute_name: value}
        try:
            return (student_profile_model.objects.filter(**data).exists() or
                    coko_profile_model.objects.filter(**data).exists())
        except Exception:
            return False

    def get_profile_or_info_by_attribute(self, attribute_name: str, value, output: str) -> Union[
        None,
        student_profile_model,
        coko_profile_model,
        str
    ]:
        """
        Получить профиля или информации по полученному значению атрибута
        :param attribute_name: наименование атрибута (поле модели профиля)
        :param value: значение
        :param output: profile - получить профиль, username - имя пользователя, display_name - ФИО пользователя
        :return: None - профиль не найден, Profile - найденный профиль, str - информация из профиля
        """
        if self.is_profile_exist(attribute_name, value):
            find = {attribute_name: value}
            if student_profile_model.objects.filter(**find).exists():
                prof = student_profile_model.objects.filter(**find).first()
            else:
                prof = coko_profile_model.objects.filter(**find).first()
            if output in ['profile', 'username', 'display_name']:
                if output == 'profile':
                    return prof
                elif output == 'username':
                   return UserUtils().get_username_by_id(prof.django_user_id)
                else:
                    return prof.get_display_name()
        return None

    @staticmethod
    def set_student_profile_data(
            prof: student_profile_model,
            data: dict
    ) -> Union[bool, str]:
        """
        Запись информации в профиль обучающегося
        :param prof: профиль обучающегося
        :param data: словарь с данными профиля
        :return: true - информация сохранена, false - данные не прошли валидацию, str - traceback системной ошибки
        """
        if ValidateUtils.validate_data(set_student_profile_fields, data):
            try:
                for key, value in data.items():
                    if key != 'state':
                        setattr(prof, key, value)
                    else:
                        state = state_model.objects.filter(name=value).first()
                        setattr(prof, key, state)
                prof.save()
                return True
            except Exception:
                return ExceptionHandling.get_traceback()
        return False

    @staticmethod
    def set_coko_profile_data(
            prof: coko_profile_model,
            data: dict
    ) -> Union[bool, str]:
        """
        Запись информации в профиль сотрудника ЦОКО
        :param prof: профиль сотрудника ЦОКО
        :param data: словарь с данными профиля
        :return: true - информация сохранена, false - данные не прошли валидацию, str - traceback сисетмной ошибки
        """
        if ValidateUtils.validate_data(set_coko_profile_fields, data):
            try:
                for key, value in data.items():
                    setattr(prof, key, value)
                prof.save()
                return True
            except Exception:
                return ExceptionHandling.get_traceback()
        return False
