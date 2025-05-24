import datetime
import os

from django.core.mail import EmailMessage

from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.commons.utils.django.settings import settings_utils
from apps.reports.services.services_chart import ServiceChart
from web_app.init_celery import app


@app.task
def email_report_service_chart(email: str, report_parameters: dict):
    """
    Задача Celery для отправки сформированного файла отчета с графиком оказанных услуг на почту
    :param email: Адрес почты для отправки файла
    :param report_parameters: Параметры для отчета по опросу
    :return:
    """

    @journal_celery_task(
        'Задача на отправку отчета с графиком оказанных услуг успешно выполнена',
        'Задача на отправку отчета графиком оказанных услуг завершилась ошибкой'
    )
    def wrapper():
        login = email.split("@")[0]
        report_folder = os.path.join(
            settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
            'Отчеты',
            'График услуг',
            login
        )
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)
        fix_time = datetime.datetime.now()
        service_chart = ServiceChart(report_parameters)
        docx = service_chart.generate_file()
        file_name = f'{login} - {fix_time.strftime("%d-%m-%Y %H-%M-%S")}.docx'
        docx.save(os.path.join(report_folder, file_name))
        message = EmailMessage(
            "АИС «Учебный центр»: График услуг",
            f"Во вложении находится сформированный график услуг",
            None,
            [email, ]
            # [settings_utils.get_parameter_from_settings('TEST_EMAIL'), ]
        )
        message.attach_file(os.path.join(report_folder, file_name))
        message.send()

    wrapper()
