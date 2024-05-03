from apps.authen.utils.profile import ProfileUtils


class RequestUtils:
    """Класс методов для работы с объектом request"""

    @staticmethod
    def get_source_display_name(request) -> str:
        """Получение наименования источника для журнала событий"""
        if request.user:
            if request.user.is_authenticated:
                return ProfileUtils().get_profile_or_info_by_attribute(
                    'django_user_id',
                    request.user.id,
                    'display_name'
                )
            return 'Неавторизованный пользователь'
        return 'Неизвестно'
