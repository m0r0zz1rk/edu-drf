import uuid

from django.db.models import QuerySet

from apps.applications.consts.application_statuses import ARCHIVE
from apps.applications.selectors.event_application import event_application_model, event_application_orm
from apps.authen.services.profile import profile_service
from apps.commons.services.ad.ad_centre import ad_centre_service
from apps.edu.selectors.program import program_queryset
from apps.edu.selectors.student_group import student_group_queryset


class EventApplicationService:
    """
    Класс методов для работы с заявками на мероприятия
    """

    _pass_fields = [
        'object_id',
        'old_id',
        'date_create',
        'group',
        'profile',
        'oo_new',
    ]

    _fk_fields = [
        'region',
        'mo',
        'position_category',
        'position',
    ]

    @staticmethod
    def get_event_app(app_id: uuid) -> event_application_model:
        """
        Получить заявку на мероприятие (ИКУ) по object_id
        :param app_id: object_id заявки на мероприятие
        :return: объект заявки на курс (EventApplication)
        """
        return event_application_orm.get_one_record_or_none({'object_id': app_id})

    @staticmethod
    def get_all_apps(profile_id: uuid) -> QuerySet:
        """
        Получение всех заявок обучающегося на курсы (для ЛК администратора)
        :param profile_id: object_id профиля обучающегося
        :return: список словарей с подразделением и его заявками обучающегося
        """
        return event_application_orm.get_filter_records(filter_by={'profile_id': profile_id})

    def get_active_apps(self, profile_id: uuid) -> QuerySet:
        """
        Получение активных заявок на мероприятия (для ЛК пользователя)
        :param profile_id: object_id профиля пользователя
        :return: QuerySet с заявками
        """
        all_apps = self.get_all_apps(profile_id)
        return all_apps.exclude(status=ARCHIVE).order_by('-date_create')

    def get_archive_apps(self, profile_id: uuid) -> QuerySet:
        """
        Получение архивных заявок на мероприятия
        :param profile_id: object_id профиля пользователя
        :return: QuerySet с заявками
        """
        all_apps = self.get_all_apps(profile_id)
        return all_apps.filter(status=ARCHIVE).order_by('-date_create')

    @staticmethod
    def get_departments_apps(user_id: int, archive: bool = False) -> list:
        """
        Получение списка заявок обучающегося по подразделениям
        :param user_id: ID пользователя Django
        :param archive: True - получение только архивных заявок
        :return: список словарей с подразделением и его заявками обучающегося
        """
        res = []
        profile = profile_service.get_profile_or_info_by_attribute(
            'django_user_id',
            user_id,
            'profile'
        )
        user_apps = event_application_orm.get_filter_records({'profile_id': profile.object_id})
        if archive:
            user_apps = user_apps.filter(status=ARCHIVE)
        groups = {group for group in user_apps.values_list('group__object_id', flat=True)}
        programs = {program for program in student_group_queryset.
        filter(object_id__in=groups).values_list('ou__program__object_id', flat=True)}
        deps = {department for department in
                program_queryset.filter(object_id__in=programs).values_list('department__object_id', flat=True)}
        for dep in deps:
            res.append({
                'department': ad_centre_service.get_ad_centre(
                    'object_id',
                    dep
                ).display_name,
                'apps': user_apps.filter(
                    group__in=student_group_queryset.filter(
                        ou__program__in=program_queryset.filter(
                            department_id=dep
                        )
                    )
                )
            })
        return res

    @staticmethod
    def get_group_apps(group_id: uuid) -> QuerySet:
        """
        Получение списка заявок в учебной группе мероприятия
        :param group_id: object_id учебной группы
        :return: QuerySet с заявками
        """
        return event_application_orm.get_filter_records(filter_by={'group_id': group_id})

    @staticmethod
    def get_total_apps_count() -> int:
        """
        Получение общего количества заявок на курсы в БД
        :return: количество
        """
        return event_application_orm.get_filter_records().count()


event_application_service = EventApplicationService()
