import datetime
from pandas._libs.tslibs.offsets import BDay

from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.edu.consts.planning_parameters import PlanningParameters
from apps.edu.consts.student_group.statuses import STATEMENT, REGISTRATION
from apps.edu.services.planning_parameter import planning_parameter_service
from apps.edu.services.student_group import student_group_service
from web_app.init_celery import app


@app.task
def check_registration_end():
    """
    Периодическая задача Celery для проверки учебных групп на предмет остановки регистрации (смены статуса)
    при условии, что осталось определенное количество дней () до начала старта
    :return:
    """

    @journal_celery_task(
        'Задача на проверку окончания регистрации успешно выполнена',
        'Задача на проверку окончания регистрации завершилась ошибкой'
    )
    def wrapper():
        groups = student_group_service.get_groups_with_status([REGISTRATION, ])
        changed = []
        for group in groups:
            date_start = group.ou.date_start if group.ou else group.iku.date_start
            delta = date_start - BDay(
                int(planning_parameter_service.get_parameter_value_by_name(PlanningParameters.STUDENT_GROUP_STATEMENT_DAYS))
            )
            if datetime.date.today() >= delta:
                student_group_service.update_group_status(group.object_id, STATEMENT)
                changed.append(group.code)
        return f'Обновлены статусы у следующих групп: {repr(changed)}'

    wrapper()
