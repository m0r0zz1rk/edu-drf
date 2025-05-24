import datetime
import os

from django.core.mail import EmailMessage

from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.commons.utils.django.settings import settings_utils
from apps.reports.services.fis_frdo import FisFrdo
from web_app.init_celery import app


@app.task
def email_report_fis_frdo(email: str, report_parameters: dict):
    """
    Задача Celery для отправки сформированного файла отчета ФИС ФРДО на почту
    :param email: Адрес почты для отправки файла
    :param report_parameters: Параметры для отчета
    :return:
    """

    @journal_celery_task(
        'Задача на отправку отчета ФИС ФРДО успешно выполнена',
        'Задача на отправку отчета ФИС ФРДО завершилась ошибкой'
    )
    def wrapper():
        login = email.split("@")[0]
        report_folder = os.path.join(
            settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
            'Отчеты',
            'ФИС ФРДО',
            login
        )
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)
        fix_time = datetime.datetime.now()
        fis_frdo_service = FisFrdo(report_parameters)
        xlsx = fis_frdo_service.generate_file()
        file_name = f'{login} - {fix_time.strftime("%d-%m-%Y %H-%M-%S")}.xlsx'
        xlsx.save(os.path.join(report_folder, file_name))
        message = EmailMessage(
            "АИС «Учебный центр»: Отчет ФИС ФРДО",
            f"Во вложении находится сформированный отчет ФИС ФРДО",
            None,
            [email, ]
            # [settings_utils.get_parameter_from_settings('TEST_EMAIL'), ]
        )
        message.attach_file(os.path.join(report_folder, file_name))
        message.send()

    wrapper()
