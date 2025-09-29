import datetime
from typing import Union

from apps.authen.services.profile import profile_service
from apps.commons.utils.django.user import user_utils
from apps.guides.selectors.profiles.coko import coko_profile_model
from apps.guides.selectors.profiles.student import student_profile_model, student_profile_orm
from apps.guides.selectors.state import state_orm


class UserService:
    """Класс методов для работы с пользователями АИС"""

    _teachers_attrs = (
        'surname',
        'name',
        'patronymic'
    )

    def get_teachers(self) -> list:
        """Получение списка преподавателей"""
        teachers = []
        for coko in coko_profile_model.objects.all():
            teacher = {
                'type': 'Сотрудник ЦОКО',
                'phone': None
            }
            for attr in self._teachers_attrs:
                teacher[attr] = getattr(coko, attr)
            teachers.append(teacher)
        for user in student_profile_orm.get_filter_records():
            teacher = {'type': 'Внешний пользователь', 'phone': user.phone}
            for attr in self._teachers_attrs:
                teacher[attr] = getattr(user, attr)
        return teachers

    @staticmethod
    def check_unique_data(serialize_data: dict, attr_name: str) -> Union[str, bool]:
        """
        Проверка на уникальность полученного значения среди всех
        профилей пользователей АИС (кроме полученного по user_id)
        :param serialize_data: полученные данные после сериализации
        :param attr_name: имя атрибута профиля на проверку
        :return: True - значение уникально, иначе False
        """
        user_id = profile_service.get_profile_or_info_by_attribute(
            'object_id',
            serialize_data['profile_id'],
            'user_id'
        )
        check = profile_service.check_unique_data_for_profile(
            user_id,
            attr_name,
            serialize_data[attr_name]
        )
        return check

    @staticmethod
    def update_profile(serialize_data: dict):
        """
        Обновление профиля пользователя
        :param serialize_data: Словарь с сериализованными данными о пользователе (UserUpdateSerializer)
        :return:
        """
        profile_id = serialize_data.get('object_id')
        del serialize_data['object_id']
        email = serialize_data.get('email')
        del serialize_data['email']
        user_id = profile_service.get_profile_or_info_by_attribute(
            'object_id',
            profile_id,
            'user_id'
        )
        user_utils.email_change(user_id, email)
        data = {}
        for k, v in serialize_data.items():
            if k == 'birthday':
                data[k] = datetime.datetime.strptime(v, '%Y-%m-%d')
            elif k == 'state':
                data[k] = state_orm.get_one_record_or_none({'name': v})
            else:
                data[k] = v
        student_profile_orm.update_record({'object_id': profile_id}, data)

    @staticmethod
    def change_password(serialize_data: dict):
        """
        Обновление пароля пользователя
        :param serialize_data: Словарь с сериализованными данными (UserChangePasswordSerializer)
        :return:
        """
        user_id = profile_service.get_profile_or_info_by_attribute(
            'object_id',
            serialize_data.get('profile_id'),
            'user_id'
        )
        user_utils.password_change(
            user_id,
            serialize_data.get('password')
        )


user_service = UserService()
