import uuid

from django.db.models import QuerySet

from apps.applications.consts.application_statuses import ARCHIVE
from apps.applications.selectors.course_application import course_application_model
from apps.authen.services.profile import ProfileService
from apps.commons.services.ad.ad_centre import AdCentreService
from apps.edu.selectors.program import program_queryset
from apps.edu.selectors.student_group import student_group_queryset


class CourseApplicationService:
    """Класс методов для работы с заявками обучающихся на участие в курсах"""

    _profile_service = ProfileService()
    _student_group_qs = student_group_queryset()
    _program_qs = program_queryset()
    _ad_centre_service = AdCentreService()

    _pass_fields = [
        'object_id',
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
        'education_doc',
        'surname_doc',
        'certificate_doc'
    ]

    @staticmethod
    def get_course_app(app_id: uuid) -> course_application_model:
        """
        Получить заявку на курс по object_id
        :param app_id: object_id заявки на курс
        :return: объект заявки на курс (CourseApplication)
        """
        return course_application_model.objects.get(object_id=app_id)

    def get_departments_apps(self, user_id: int, apps_queryset: QuerySet, archive: bool = False) -> list:
        """
        Получение списка заявок обучающегося по подразделениям
        :param user_id: ID пользователя Django
        :param apps_queryset: QuerySet со всем заявками на курсы
        :param archive: True - получение только архивных заявок
        :return: список словарей с подразделением и его заявками обучающегося
        """
        res = []
        profile = self._profile_service.get_profile_or_info_by_attribute(
            'django_user_id',
            user_id,
            'profile'
        )
        user_apps = apps_queryset.filter(profile_id=profile.object_id)
        if archive:
            user_apps = user_apps.filter(status=ARCHIVE)
        groups = {group for group in user_apps.values_list('group__object_id', flat=True)}
        programs = {program for program in self._student_group_qs.
                    filter(object_id__in=groups).values_list('ou__program__object_id', flat=True)}
        deps = {department for department in
                self._program_qs.filter(object_id__in=programs).values_list('department__object_id', flat=True)}
        for dep in deps:
            res.append({
                'department': self._ad_centre_service.get_ad_centre(
                    'object_id',
                    dep
                ).display_name,
                'apps': user_apps.filter(
                    group__in=self._student_group_qs.filter(
                        ou__program__in=self._program_qs.filter(
                            department_id=dep
                        )
                    )
                )
            })
        return res

    def save_app(self, app_id: uuid, app_info: dict):
        """
        Сохранение информации по заявке
        :param app_id: object_id изменяемой заявки
        :param app_info: словарь с информацией по заявке
        """
        app = self.get_course_app(app_id)
        updated_app = {
            'group_id': app.group_id,
            'profile_id': app.profile_id
        }
        for field in course_application_model._meta.get_fields():
            if field.name in self._pass_fields:
                continue
            if field.name in self._fk_fields:
                updated_app[field.name+'_id'] = app_info.get(field.name+'_object_id')
            elif field.name == 'oo':
                if app_info.get('oo_new') != '':
                    updated_app[field.name+'_id'] = None
                    updated_app[field.name+'_new'] = app_info.get('oo_new')
                else:
                    updated_app[field.name+'_id'] = app_info.get('oo_object_id')
                    updated_app[field.name+'_new'] = ''
            else:
                updated_app[field.name] = app_info.get(field.name)
        print(updated_app)
        course_application_model.objects.update_or_create(
            object_id=app_id,
            defaults={**updated_app}
        )
