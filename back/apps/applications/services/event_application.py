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
    def get_course_app(app_id: uuid) -> event_application_model:
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

    def save_app(self, app_id: uuid, app_info: dict):
        """
        Сохранение информации по заявке
        :param app_id: object_id изменяемой заявки
        :param app_info: словарь с информацией по заявке
        """
        app = self.get_course_app(app_id)
        updated_app = {
            'group_id': app.group_id,
            'profile_id': app.profile_id,
            'old_id': app.old_id
        }
        for field in event_application_model._meta.get_fields():
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
        event_application_orm.update_record(
            filter_by={'object_id': app_id},
            update_object=updated_app
        )


event_application_service = EventApplicationService()
