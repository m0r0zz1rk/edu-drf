import uuid
from typing import Optional

from django.db.models import QuerySet

from apps.applications.consts.application_statuses import ARCHIVE, DRAFT
from apps.applications.selectors.course_application import course_application_model, course_application_orm
from apps.authen.services.profile import profile_service
from apps.commons.services.ad.ad_centre import ad_centre_service
from apps.edu.selectors.program import program_queryset
from apps.edu.selectors.student_group import student_group_queryset


class CourseApplicationService:
    """Класс методов для работы с заявками обучающихся на участие в курсах"""

    _pass_fields = [
        'object_id',
        'old_id',
        'date_create',
        'group',
        'profile',
        'oo_new',
        'coursecertificate'
    ]

    _fk_fields = [
        'region',
        'mo',
        'position_category',
        'position',
        'education_doc',
        'surname_doc',
        'certificate_doc'
    ]

    @staticmethod
    def get_course_app(app_id: uuid) -> Optional[course_application_model]:
        """
        Получить заявку на курс по object_id
        :param app_id: object_id заявки на курс
        :return: объект заявки на курс (CourseApplication) или None
        """
        return course_application_orm.get_one_record_or_none({'object_id': app_id})

    @staticmethod
    def get_all_apps(profile_id: uuid) -> QuerySet:
        """
        Получение всех заявок обучающегося на курсы (для ЛК администратора)
        :param profile_id: object_id профиля обучающегося
        :return: список словарей с подразделением и его заявками обучающегося
        """
        return course_application_orm.get_filter_records(filter_by={'profile_id': profile_id})

    def get_active_apps(self, profile_id: uuid) -> QuerySet:
        """
        Получение активных заявок на курсы (для ЛК пользователя)
        :param profile_id: object_id профиля пользователя
        :return: QuerySet с заявками
        """
        all_apps = self.get_all_apps(profile_id)
        return all_apps.exclude(status=ARCHIVE).order_by('-date_create')

    def get_last_app(self, profile_id: uuid) -> Optional[course_application_model]:
        """
        Получение крайней заявки обучающегося на курс со стаусом не равным "Черновик"
        :param profile_id: object_id профиля обучающегося
        :return: Заявка или None (в случае если заявки нет)
        """
        all_apps = self.get_all_apps(profile_id)
        if all_apps.count() > 0:
            not_draft_apps = all_apps.exclude(status=DRAFT)
            if not_draft_apps.count() > 0:
                return not_draft_apps.order_by('-date_create').first()

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
        user_apps = course_application_orm.get_filter_records({'profile_id': profile.object_id})
        if archive:
            user_apps = user_apps.filter(status=ARCHIVE)
        groups = {group for group in user_apps.values_list('group__object_id', flat=True)}
        programs = {program for program in student_group_queryset().
            filter(object_id__in=groups).values_list('ou__program__object_id', flat=True)}
        deps = {department for department in
                program_queryset().filter(object_id__in=programs).values_list('department__object_id', flat=True)}
        for dep in deps:
            res.append({
                'department': ad_centre_service.get_ad_centre(
                    'object_id',
                    dep
                ).display_name,
                'apps': user_apps.filter(
                    group__in=student_group_queryset().filter(
                        ou__program__in=program_queryset().filter(
                            department_id=dep
                        )
                    )
                )
            })
        return res

    @staticmethod
    def get_group_apps(group_id: uuid) -> QuerySet:
        """
        Получение списка заявок в учебной группе курса
        :param group_id: object_id учебной группы
        :return: QuerySet с заявками
        """
        return course_application_orm.get_filter_records(
            filter_by={'group_id': group_id},
            exclude={'status': DRAFT},
            order_by=['profile__surname', 'profile__name', 'profile__patronymic']
        )

    @staticmethod
    def get_total_apps_count() -> int:
        """
        Получение общего количества заявок на курсы в БД
        :return: количество
        """
        return course_application_orm.get_filter_records().count()

    @staticmethod
    def get_last_active_app(user_id: int) -> Optional[course_application_model]:
        """
        Получение крайней активной заявки у обучающегося
        :param user_id: ID пользователя Django
        :return: Последняя активная заявки или None, если таковых нет
        """


course_application_service = CourseApplicationService()
