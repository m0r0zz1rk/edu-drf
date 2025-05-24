import datetime
import os

from django.core.mail import EmailMessage

from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.commons.utils.django.settings import settings_utils
from apps.surveys.services.survey_report import SurveyReportService
from web_app.init_celery import app


@app.task
def email_survey_report(email: str, report_parameters: dict):
    """
    Задача Celery для отправки сформированного файла отчета по опросу на почту
    :param email: Адрес почты для отправки файла
    :param report_parameters: Параметры для отчета по опросу
    :return:
    """

    @journal_celery_task(
        'Задача на отправку отчета по опросу успешно выполнена',
        'Задача на отправку отчета по опросу завершилась ошибкой'
    )
    def wrapper():
        report_folder = os.path.join(
            settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
            'Отчеты по опросам'
        )
        fix_time = datetime.datetime.now()
        survey_report_service = SurveyReportService(report_parameters)
        wb = survey_report_service.generate_report()
        file_name = f'{email.split("@")[0]} - {fix_time.strftime("%d-%m-%Y %H-%M-%S")}.xlsx'
        wb.save(os.path.join(report_folder, file_name))
        message = EmailMessage(
            "АИС «Учебный центр»: Отчет по результатам опроса",
            f"Во вложении находится сформированный отчет по результатам опроса",
            None,
            [email, ]
            # [settings_utils.get_parameter_from_settings('TEST_EMAIL'), ]
        )
        message.attach_file(os.path.join(report_folder, file_name))
        message.send()

    wrapper()
