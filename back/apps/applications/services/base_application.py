import uuid

from django.db.models import Model

from apps.applications.exceptions.application import ApplicationCreateError
from apps.applications.selectors.course_application import course_application_model
from apps.applications.selectors.event_application import event_application_model
from apps.authen.services.profile import profile_service
from apps.guides.selectors.region import irkutsk_state_object


class BaseApplicationService:
    """
    Класс методов для работы с заявками
    """

    def create_app(self, user_id: int, group_id: uuid, application_model: Model) -> uuid:
        """
        Создание заявки
        :param user_id: ID пользователя Django
        :param group_id: object_id учебной группы
        :param application_model: модель заявок (CourseApplication или EventApplication)
        :return: object_id созданной заявки
        """
        try:
            profile = profile_service.get_profile_or_info_by_attribute(
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

    @staticmethod
    def apps_count() -> int:
        """
        Получение общего количества заявок в АИС
        """
        return course_application_model.objects.count() + event_application_model.objects.count()

    @staticmethod
    def get_app_count_for_group(group_id: uuid, course_group: bool) -> int:
        """
        Получение количества заявок для учебной группы
        :param group_id: object_id учебной группы
        :param course_group: группа для ОУ (курса)
        :return: количество заявок
        """
        if course_group:
            return course_application_model.objects.filter(group_id=group_id).count()
        return event_application_model.objects.filter(group_id=group_id).count()


base_application_service = BaseApplicationService()
