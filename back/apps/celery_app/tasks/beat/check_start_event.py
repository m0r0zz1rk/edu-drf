import datetime

from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.edu.consts.student_group.statuses import PROCESS, OFFER, URL, STATEMENT, REGISTRATION
from apps.edu.selectors.student_group import student_group_orm
from apps.edu.services.student_group import student_group_service
from web_app.init_celery import app


@app.task
def check_start_event():
    """
    Периодическая задача Celery для проверки начала проведения курса/мероприятия учебной группы
    Если дата начала наступила, то меняем статус групп на "Идет обучение"
    :return:
    """

    @journal_celery_task(
        'Задача на проверку начала мероприятия успешно выполнена',
        'Задача на проверку начала мероприятия завершилась ошибкой'
    )
    def wrapper():
        groups = student_group_service.get_groups_with_status([REGISTRATION, OFFER, URL, STATEMENT])
        updated = []
        for group in groups:
            date_start = group.ou.date_start if group.ou else group.iku.date_start
            if datetime.date.today() >= date_start:
                student_group_orm.update_record(
                    filter_by=dict(object_id=group.object_id),
                    update_object={'status': PROCESS}
                )
                updated.append(group.code)
        return f'Обновлены статусы у следующих групп: {repr(updated)}'
    wrapper()
