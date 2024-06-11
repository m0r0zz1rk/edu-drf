from apps.authen.services.profile import ProfileService
from apps.commons.utils.django.user import UserUtils


class MainPageService:
    """Класс методов для получения информации на главную страницу ЛК администратора АИС"""

    pu = ProfileService()
    uu = UserUtils()

    def get_information(self, request) -> dict:
        """
        Получение информации для главной страницы
        :param request: Объект запроса request
        :return: словарь с данными
        """
        return {
            'user_info': {
                'display_name': self.pu.get_profile_or_info_by_attribute(
                    'django_user_id',
                    request.user.id,
                    'display_name'
                ),
                'first_login': self.uu.get_user_date_joined(request.user.id)
            },
            'study_info': {
                'user_count': 15,
                'app_count': 27,
                'course_count': 8,
                'event_count': 10
            },
            'last_apps': [
                {
                    'user': 'Морозов Никита Дмитриевич',
                    'event_name': 'Мероприятие-справочник по проведение внутренних гос. экзаменов',
                    'status': 'Черновик'
                },
                {
                    'user': 'Абобов Валерий Валакасович',
                    'event_name': 'Курс повышения квалификации по сдаче ЕГЭ',
                    'status': 'Подтверждена'
                },
            ]
        }

