from apps.applications.services.base_application import BaseApplicationService
from apps.authen.selectors.user import user_orm
from apps.authen.services.profile import ProfileService
from apps.commons.services.ad.ad_centre_coko_user import ad_centre_coko_user_utils
from apps.commons.utils.django.user import UserUtils
from apps.edu.services.service.education_service import EducationServiceService
from apps.edu.services.service.information_service import InformationServiceService


class MainPageService:
    """
    Класс методов для получения информации на
    главную страницу ЛК администратора АИС
    """

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
                'dep': ad_centre_coko_user_utils.get_user_centre_display_name(request.user),
                'first_login': self.uu.get_user_date_joined(request.user.id)
            },
            'study_info': {
                'user_count': user_orm.get_all_objects_count(),
                'app_count': BaseApplicationService.apps_count(),
                'course_count': EducationServiceService.get_count(),
                'event_count': InformationServiceService.get_count()
            },
            'last_apps': [
                {
                    'user': 'Морозов Никита Дмитриевич',
                    'event_name': 'Мероприятие-справочник по '
                                  'проведение внутренних гос. '
                                  'экзаменов',
                    'status': 'Черновик'
                },
                {
                    'user': 'Абобов Валерий Валакасович',
                    'event_name': 'Курс повышения квалификации '
                                  'по сдаче ЕГЭ',
                    'status': 'Подтверждена'
                },
            ]
        }
