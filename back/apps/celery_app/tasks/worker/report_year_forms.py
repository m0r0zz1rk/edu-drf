import datetime
import os

from django.core.mail import EmailMessage

from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.commons.utils.django.settings import settings_utils
from apps.reports.services.year_forms import YearFormsReport
from web_app.init_celery import app


@app.task
def email_report_year_forms(email: str, report_parameters: dict):
    """
    Задача Celery для отправки сформированного файла с данным об анкетах за год
    :param email: Адрес почты для отправки файла
    :param report_parameters: Параметры для отчета
    :return:
    """

    @journal_celery_task(
        'Задача на отправку анкет за год успешно выполнена',
        'Задача на отправку анкет за год завершилась ошибкой'
    )
    def wrapper():
        login = email.split("@")[0]
        report_folder = os.path.join(
            settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
            'Отчеты',
            'Анкеты за год',
            login
        )
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)
        fix_time = datetime.datetime.now()
        year_forms_service = YearFormsReport(report_parameters)
        xlsx = year_forms_service.generate_file()
        file_name = f'{login} - {fix_time.strftime("%d-%m-%Y %H-%M-%S")}.xlsx'
        xlsx.save(os.path.join(report_folder, file_name))
        message = EmailMessage(
            f"АИС «Учебный центр»: Анкеты за {report_parameters.get('report_year')} год",
            f"Во вложении находится сформированный файл с данными по "
            f"анкетам за {report_parameters.get('report_year')} год",
            None,
            [email, ]
            # [settings_utils.get_parameter_from_settings('TEST_EMAIL'), ]
        )
        message.attach_file(os.path.join(report_folder, file_name))
        message.send()

    wrapper()
