import datetime
import os

from django.core.mail import EmailMessage

from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.commons.utils.django.settings import settings_utils
from apps.reports.services.pk_one_report import PKOneReport
from web_app.init_celery import app


@app.task
def email_report_pk_one(email: str, report_parameters: dict):
    """
    Задача Celery для отправки сформированного файла отчета ПК-1 на почту
    :param email: Адрес почты для отправки файла
    :param report_parameters: Параметры для отчета по опросу
    :return:
    """

    @journal_celery_task(
        'Задача на отправку отчета ПК-1 успешно выполнена',
        'Задача на отправку отчета ПК-1 завершилась ошибкой'
    )
    def wrapper():
        login = email.split("@")[0]
        report_folder = os.path.join(
            settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
            'Отчеты',
            'ПК-1',
            login
        )
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)
        fix_time = datetime.datetime.now()
        dpp_report_service = PKOneReport(report_parameters)
        xlsx = dpp_report_service.generate_file()
        file_name = f'{login} - {fix_time.strftime("%d-%m-%Y %H-%M-%S")}.xlsx'
        xlsx.save(os.path.join(report_folder, file_name))
        message = EmailMessage(
            "АИС «Учебный центр»: Отчет ПК-1",
            f"Во вложении находится сформированный отчет ПК-1",
            None,
            # [email, ]
            [settings_utils.get_parameter_from_settings('TEST_EMAIL'), ]
        )
        message.attach_file(os.path.join(report_folder, file_name))
        message.send()

    wrapper()
