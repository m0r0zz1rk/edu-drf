from typing import Union

from apps.authen.services.profile import ProfileService
from apps.guides.selectors.coko import coko_profile_model
from apps.guides.selectors.user import student_profile_model


class UserService:
    """Класс методов для работы с пользователями АИС"""

    _profile_service = ProfileService()

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
        for user in (student_profile_model.
                     select_related('django_user').
                     select_related('state').
                     objects.all()):
            teacher = {
                'type': 'Внешний пользователь',
                'phone': user.phone
            }
            for attr in self._teachers_attrs:
                teacher[attr] = getattr(user, attr)
        return teachers

    def check_unique_data(
        self,
        request_data: dict,
        serializer,
        attr_name: str,
    ) -> Union[str, bool]:
        """
        Проверка на уникальность полученного значения среди всех
        профилей пользователей АИС (кроме полученного по user_id)
        :param request_data: полученные данные из request
        :param serializer: сериализатор для обработки входящих данных из request
        :param attr_name: имя атрибута профиля на проверку
        :return: True - значение уникально,
                 False - значение используется другим пользователем,
                 str - ошибки сериализации
        """
        serialize = serializer(data=request_data)
        if serialize.is_valid():
            check = self._profile_service.check_unique_data_for_profile(
                self._profile_service.get_profile_or_info_by_attribute(
                    'object_id',
                    serialize.data['profile_id'],
                    'user_id'
                ),
                attr_name,
                serialize.data[attr_name]
            )
            return check
        else:
            return serialize.errors
