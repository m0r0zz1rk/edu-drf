from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.commons.utils.ldap import ldap_utils
from web_app.init_celery import app


@app.task
def get_ad_and_old_data():
    """
    Периодическая задача Celery для получения информации по подразделениям из Active Directory
    :return:
    """

    @journal_celery_task(
        'Задача на получение АД выполнена',
        'Задача на получение АД завершилась ошибкой'
    )
    def wrapper():
        ldap_utils.set_ad_centres()
    wrapper()
