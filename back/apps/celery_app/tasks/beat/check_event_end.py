from apps.applications.consts.application_statuses import STUDY_COMPLETE, ARCHIVE
from apps.applications.services.course_application import course_application_service
from apps.applications.services.event_application import event_application_service
from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.edu.consts.student_group.statuses import COMPLETE
from apps.edu.services.student_group import student_group_service
from web_app.init_celery import app


@app.task
def check_event_end():
    """
    Периодическая задача в Celery для проверки окончания курса/мероприятия
    Есть событие завершено, то все заявки перевести в статус "Обучение завершено"
    """
    @journal_celery_task(
        'Задача на изменение статуса заявок завершенного события успешно выполнена',
        'Задача на изменение статуса заявок завершенного события завершилась ошибкой'
    )
    def wrapper():
        groups = student_group_service.get_groups_with_status([COMPLETE])
        app_update_count = 0
        for group in groups:
            apps = course_application_service.get_group_apps(group.object_id) if group.ou else \
                event_application_service.get_group_apps(group.object_id)
            for application in apps.exclude(status__in=[STUDY_COMPLETE, ARCHIVE]):
                application.status = STUDY_COMPLETE
                application.save()
                app_update_count += 1
        return f'Количество обновленных заявок: {app_update_count}'
    wrapper()
