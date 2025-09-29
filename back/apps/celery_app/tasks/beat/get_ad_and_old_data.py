from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.commons.services.old_edu.get_data import get_all_edu_data
from apps.commons.utils.ldap import ldap_utils
from web_app.init_celery import app


@app.task
def get_ad_and_old_data():
    """
    Периодическая задача Celery для получения информации по подразделениям из Active Directory
    и данных из БД старой версии АИС
    :return:
    """

    @journal_celery_task(
        'Задача на получение АД и старых данных выполнена',
        'адача на получение АД и старых данных завершилась ошибкой'
    )
    def wrapper():
        ldap_utils.set_ad_centres()
        get_all_edu_data()
    wrapper()
