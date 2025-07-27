import datetime

from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.edu.consts.student_group.statuses import PROCESS
from apps.edu.services.student_group import student_group_service
from web_app.init_celery import app


@app.task
def show_survey():
    """
    Периодическая задача Celery для отображения ссылки на опрос в учебной группе
    за один день до окончания мероприятия
    :return:
    """

    @journal_celery_task(
        'Задача на проверку отображения опроса успешно выполнена',
        'Задача на проверку отображения опроса завершилась ошибкой'
    )
    def wrapper():
        groups = student_group_service.get_groups_with_status([PROCESS, ])
        changed = []
        for group in groups:
            date_end = group.ou.date_end if group.ou else group.iku.date_end
            delta = date_end - datetime.date.today()
            if delta.days <= 1:
                student_group_service.show_group_survey(group.object_id)
                changed.append(group.code)
        return f'Опросы отображены у следующих групп: {repr(changed)}'

    wrapper()
