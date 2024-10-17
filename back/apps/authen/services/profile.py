from typing import Union, Optional
from django.contrib.auth.models import User

from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.user import UserUtils
from apps.commons.utils.validate import ValidateUtils
from apps.guides.selectors.coko import coko_profile_model
from apps.guides.selectors.state import state_model
from apps.guides.selectors.user import student_profile_model


class ProfileService:
    """Класс методов для работы с профилями пользователей"""

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
        'internal_phone',
        'curator_groups'
    ]

    uu = UserUtils()

    def is_profile_exist(self, attribute_name: str, value) -> bool:
        """
        Проверка на существующий профиль пользователя по заданному атрибуту и его значению
        :param attribute_name: наименование атрибута (поле модели профиля)
        :param value: значение
        :return: true - профиль существует, false - профиль не существует
        """
        data = {attribute_name: value}
        try:
            return (student_profile_model.objects.
                    select_related('django_user').
                    select_related('state').
                    filter(**data).exists() or
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
        :param output:
            profile - получить профиль,
            username - имя пользователя,
            display_name - ФИО пользователя,
            email - Email пользователя,
            user_id - ID пользователя Django,
            phone - Телефон пользователя
        :return: None - профиль не найден, Profile - найденный профиль, str - информация из профиля
        """
        if self.is_profile_exist(attribute_name, value):
            find = {attribute_name: value}
            if (student_profile_model.objects.
                    select_related('django_user').
                    select_related('state').
                    filter(**find).exists()):
                prof = (student_profile_model.objects.
                        select_related('django_user').
                        select_related('state').
                        filter(**find).first())
            else:
                prof = coko_profile_model.objects.select_related('django_user').filter(**find).first()
            if output in ['profile', 'username', 'display_name', 'email', 'phone', 'user_id']:
                if output == 'profile':
                    return prof
                elif output == 'username':
                    return UserUtils().get_username_by_id(prof.django_user_id)
                elif output == 'user_id':
                    return prof.django_user_id
                elif output == 'email':
                    return prof.django_user.email
                elif output == 'phone':
                    return prof.internal_phone
                else:
                    return prof.display_name
        return None

    def set_student_profile_data(
            self,
            prof: student_profile_model,
            data: dict
    ) -> Union[bool, str]:
        """
        Запись информации в профиль обучающегося
        :param prof: профиль обучающегося
        :param data: словарь с данными профиля
        :return: true - информация сохранена, false - данные не прошли валидацию, str - traceback системной ошибки
        """
        if ValidateUtils.validate_data(self.set_student_profile_fields, data):
            try:
                for key, value in data.items():
                    if key == 'state':
                        state = state_model.objects.filter(name=value).first()
                        setattr(prof, key, state)
                    elif key == 'email':
                        user = User.objects.get(id=prof.django_user_id)
                        setattr(user, key, value)
                        user.save()
                    else:
                        if getattr(prof, key) != value:
                            setattr(prof, key, value)
                prof.save()
                return True
            except Exception:
                return ExceptionHandling.get_traceback()
        return False

    def set_coko_profile_data(
            self,
            prof: coko_profile_model,
            data: dict
    ) -> Union[bool, str]:
        """
        Запись информации в профиль сотрудника ЦОКО
        :param prof: профиль сотрудника ЦОКО
        :param data: словарь с данными профиля
        :return: true - информация сохранена, false - данные не прошли валидацию, str - traceback системной ошибки
        """
        if ValidateUtils.validate_data(self.set_coko_profile_fields, data):
            try:
                for key, value in data.items():
                    setattr(prof, key, value)
                prof.save()
                return True
            except Exception:
                return ExceptionHandling.get_traceback()
        return False

    def get_profile_main_page_info(self, user_id: int) -> Optional[dict]:
        """
        Получение информации из профиля пользователя для главной страницы по полученнмому ID пользователя
        :param user_id: id пользователя Django
        :return: словарь с информацией из профиля, None - профиль не найден
        """
        if self.is_profile_exist('django_user_id', user_id):
            prof = self.get_profile_or_info_by_attribute(
                'django_user_id',
                user_id,
                'profile'
            )
            user = self.uu.get_user('id', user_id)
            return {
                'fio': prof.display_name,
                'email': user.email,
                'phone': prof.phone,
                'snils': prof.snils
            }
        return None

    def check_unique_data_for_profile(self, user_id: int, attr_name: str, value: str) -> bool:
        """
        Проверка на уникальность полученного поля и его значения для пользователей
        :param user_id: ID пользователя Django
        :param attr_name: атрибут (phone, email или snils)
        :param value: значение атрибута
        :return: True - значение уникально, False - используется другим пользователей
        """
        if self.is_profile_exist('django_user_id', user_id):
            if attr_name != 'email':
                if self.is_profile_exist(attr_name, value):
                    if self.get_profile_or_info_by_attribute(
                        attr_name,
                        value,
                        'user_id'
                    ) != user_id:
                        return False
                return True
            else:
                if User.objects.filter(email=value).exists():
                    if User.objects.filter(email=value).first().id != user_id:
                        return False
                return True
        return False
