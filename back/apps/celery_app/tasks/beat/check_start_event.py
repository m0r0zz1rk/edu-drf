import datetime

from apps.applications.consts.application_statuses import WORK, WAIT_PAY, CHECK, PAY, STUDY
from apps.applications.selectors.course_application import course_application_orm
from apps.applications.selectors.event_application import event_application_orm
from apps.applications.services.base_application import base_application_service
from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.edu.consts.student_group.statuses import PROCESS, OFFER, URL, STATEMENT
from apps.edu.services.student_group import student_group_service
from web_app.init_celery import app


@app.task
def check_start_event():
    """
    Периодическая задача Celery для проверки начала проведения курса/мероприятия учебной группы
    Если дата начала наступила, то меняем статус всех заявок в группе на "Проходит обучение"
    :return:
    """

    @journal_celery_task(
        'Задача на проверку начала мероприятия успешно выполнена',
        'Задача на проверку начала мероприятия завершилась ошибкой'
    )
    def wrapper():
        groups = student_group_service.get_groups_with_status([PROCESS, OFFER, URL, STATEMENT])
        updated = []
        for group in groups:
            date_start = group.ou.date_start if group.ou else group.iku.date_start
            if datetime.date.today() >= date_start:
                orm = course_application_orm if group.ou else event_application_orm
                apps = base_application_service.get_group_apps(group.object_id, orm)
                for group_app in apps:
                    if group_app.status in [WORK, WAIT_PAY, CHECK, PAY]:
                        orm.update_record(
                            filter_by=dict(object_id=group_app.object_id),
                            update_object={'status': STUDY}
                        )
                updated.append(group.code)
        return f'Обновлены статусы заявок на "Проходит обучение" у следующих групп: {repr(updated)}'

    wrapper()
