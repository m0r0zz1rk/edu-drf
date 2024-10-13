import uuid

from django.db.models import Model

from apps.applications.exceptions.application import ApplicationCreateError
from apps.authen.services.profile import ProfileService
from apps.guides.selectors.region import irkutsk_state_object


class BaseApplicationService:
    """
    Класс методов для работы с заявками
    """

    _profile_service = ProfileService()

    def create_app(self, user_id: int, group_id: uuid, application_model: Model) -> uuid:
        """
        Создание заявки
        :param user_id: ID пользователя Django
        :param group_id: object_id учебной группы
        :param application_model: модель заявок (CourseApplication или EventApplication)
        :return: object_id созданной заявки
        """
        try:
            profile = self._profile_service.get_profile_or_info_by_attribute(
                'django_user_id',
                user_id,
                'profile'
            )
            new_app, _ = application_model.objects.update_or_create(
                profile_id=profile.object_id,
                group_id=group_id,
                region=irkutsk_state_object(),
            )
            return new_app.object_id
        except Exception:
            raise ApplicationCreateError
