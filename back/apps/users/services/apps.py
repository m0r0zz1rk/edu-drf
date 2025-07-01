from apps.applications.consts.application_statuses import ACTIVE_STATUSES
from apps.applications.selectors.course_application import course_application_orm
from apps.applications.selectors.event_application import event_application_orm
from apps.authen.selectors.student_profile import student_profile_orm


class AppsService:
    """Класс методов для работы с заявками пользователей"""

    @staticmethod
    def get_active_apps(user_id: int) -> list:
        """
        Получение списка активных заявок для обучающегося
        :param user_id: id пользователя Django
        :return: список активных заявок, содержащий: id заявки, тип, наименование, статус
        """
        apps = []
        profile = student_profile_orm.get_one_record_or_none(filter_by=dict(django_user_id=user_id))
        if profile:
            for orm in (course_application_orm, event_application_orm):
                active = orm.get_filter_records(
                    filter_by=dict(status__in=ACTIVE_STATUSES, profile_id=profile.object_id),
                    order_by=['-date_create']
                )
                if active.count() > 0:
                    app = active.first()
                    name = app.group.ou.program.name if app.group.ou else app.group.iku.name
                    app_type = 'course' if app.group.ou else 'event'
                    apps.append({
                        'object_id': app.object_id,
                        'app_type': app_type,
                        'name': name,
                        'status': app.status
                    })
        return apps


apps_service = AppsService()
