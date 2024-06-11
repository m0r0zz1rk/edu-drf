from apps.authen.services.profile import ProfileService


class RequestUtils:
    """Класс методов для работы с объектом request"""

    @staticmethod
    def get_source_display_name(request) -> str:
        """Получение наименования источника для журнала событий"""
        if request.user:
            if request.user.is_authenticated:
                return ProfileService().get_profile_or_info_by_attribute(
                    'django_user_id',
                    request.user.id,
                    'display_name'
                )
            return 'Неавторизованный пользователь'
        return 'Неизвестно'

    @staticmethod
    def convert_form_data_data(request_data: dict) -> dict:
        """
        Преобразование переменных, переданных через FormData со стороны фронта
        :param request_data: словарь request.data
        :return: скорректированный словарь
        """
        source_dict = dict(request_data)
        for key, value in source_dict.items():
            if value[0] == "null":
                source_dict[key] = None
            else:
                source_dict[key] = value[0]
        return source_dict
