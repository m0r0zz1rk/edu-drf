from datetime import datetime
import random
from typing import Optional, Union

from django.contrib.auth.models import User

from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.group import GroupUtils
from apps.commons.utils.transliterate import TransliterateUtils
from apps.commons.utils.validate import ValidateUtils


class UserUtils:
    """Класс методов для работы с моделью пользователей Django"""

    @staticmethod
    def is_user_exists(attribute_name: str, value) -> bool:
        """
        Проверка наличия пользователя в БД по полученному значению атрибута
        :param attribute_name: наименование атрибута (поле модели User)
        :param value: значение
        :return: true - пользователь существует, false - пользователь не существует
        """
        find = {attribute_name: value}
        return User.objects.filter(**find).exists()

    def get_user(self, attribute_name: str, value) -> Optional[User]:
        """
        Получение пользователя по полученному значению атрибута
        :param attribute_name: наименование атрибута (поле модели User)
        :param value: значение
        :return: None - пользователь не найден, User - найденный пользователь
        """
        if self.is_user_exists(attribute_name, value):
            find = {attribute_name: value}
            return User.objects.filter(**find).first()
        return None

    @staticmethod
    def generate_username(surname: str, name: str, patronymic: str) -> str:
        """
        Генерация имени пользователя АИС
        :param surname: Фамилия
        :param name: Имя
        :param patronymic: Отчество
        :return: Сгенерированное имя пользователя
        """
        tu = TransliterateUtils()
        username = f'{tu.translit(surname)}.{tu.translit(name)[:1]}'
        if len(patronymic) > 0:
            username += f'.{tu.translit(patronymic)[:1]}'
        while User.objects.filter(username=username).exists():
            username += str(random.randint(1, 1000))
        return username

    def get_username_by_id(self, user_id: int) -> Optional[str]:
        """
        Получение имени пользователя по id пользователя
        :param user_id: id пользователя
        :return: None - пользователь не найден, str - имя пользователя
        """
        if self.is_user_exists('id', user_id):
            return User.objects.get(id=user_id).username
        return None

    def get_username_by_email(self, email: str) -> Optional[str]:
        """
        Получение имени пользователя по email пользователя
        :param email: полученный email
        :return: None - пользователь не найден, str - имя пользователя
        """
        if self.is_user_exists('email', email):
            return User.objects.filter(email=email).first().username
        return None

    @staticmethod
    def create_new_user(data: dict) -> Union[bool, str]:
        """
        Создание нового пользователя
        :param data: информация о пользователе (email, username, password)
        :return: true - пользователь создан, false - ошибка валидации, str - traceback при ошибки в процессе создания
        """
        if ValidateUtils.validate_data(
            ['email', 'username', 'password'],
            data
        ):
            try:
                User.objects.create_user(**data)
                return True
            except Exception:
                return ExceptionHandling.get_traceback()
        return False

    def delete_user_by_username(self, username: str):
        """
        Удаление пользователя по полученному имени
        :param username: имя пользователя
        :return:
        """
        if self.is_user_exists('username', username):
            User.objects.get(username=username).delete()

    def is_user_in_group(self, user_attr: str, attr_value, group_name: str) -> Optional[bool]:
        """
        Проверка наличия пользователя в группе по его атрибуту
        :param user_attr: атрибут пользователя (username, email)
        :param attr_value: значение атрибута
        :param group_name: имя группы
        :return: True - пользователь найден в группе,
                 False - пользователь не найден в группе,
                 None - пользователь не найден
        """
        user = self.get_user(user_attr, attr_value)
        if user is None:
            return None
        return user.groups.filter(name=group_name).exists()

    def add_user_to_group(self, user_attr: str, attr_value, group_name: str):
        """
        Добавление пользователя в группу
        :param user_attr: атрибут пользователя (username, email)
        :param attr_value: значение атрибута
        :param group_name: имя группы
        :return:
        """
        if self.is_user_in_group(user_attr, attr_value, group_name) is False:
            GroupUtils().get_group_by_name(group_name).user_set.add(
                self.get_user(user_attr, attr_value)
            )

    def get_user_role_by_id(self, user_id: int) -> Optional[str]:
        """
        Получение роли пользователя по полученному ID
        :param user_id: ID пользователя
        :return: centre - Администратор, dep - сотрудник подразделения, student - обучающийся, None - не найдено
        """
        if self.is_user_exists('id', user_id):
            if User.objects.get(id=user_id).groups.exists():
                group_name = User.objects.prefetch_related('groups').get(id=user_id).groups.first().name
                if group_name == 'Администраторы':
                    return 'centre'
                elif group_name == 'Сотрудники':
                    return 'dep'
                else:
                    return 'student'
        return None

    def password_change(self, user_id: int, password: str) -> bool:
        """
        Смена пароля у пользователя
        :param user_id: ID пользователя Django
        :param password: новый пароль
        :return: True - пароль изменен, False - пароль не изменен
        """
        user = self.get_user('id', user_id)
        if user is not None:
            user.set_password(password)
            user.save()
            return True
        return False

    def get_user_date_joined(self, user_id: int) -> Optional[datetime]:
        """
        Получение даты первого входа в АИС пользователя
        :param user_id: ID пользователя Django
        :return: None - пользователь не найден, datetime - дата первого входа в АИС
        """
        user = self.get_user('id', user_id)
        if user is not None:
            return user.date_joined
        return None
