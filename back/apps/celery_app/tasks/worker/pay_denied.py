import uuid

from django.core.mail import send_mail

from apps.applications.services.course_application import course_application_service
from apps.applications.services.event_application import event_application_service
from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.commons.utils.django.settings import settings_utils
from web_app.init_celery import app


@app.task
def email_pay_denied(app_id: uuid, message: str):
    """
    Задача Celery на отправку письма об отказе в оплате участия на мероприятии обучающемуся
    :param app_id: object_id заявки
    :param message: Сообщение от сотрудника центра
    :return:
    """

    @journal_celery_task(
        'Задача на отправку сообщения об отказе оплаты выполнена',
        'Задача на отправку сообщения об отказе оплаты завершилась ошибкой'
    )
    def wrapper():
        application = course_application_service.get_course_app(app_id)
        if not application:
            application = event_application_service.get_event_app(app_id)
        subject = 'АИС "Учебный Центр": Оплата не подтверждена'
        group_type = 'курсе' if application.group.ou else 'мероприятии'
        name = application.group.ou.program.name if application.group.ou else application.group.event.name
        url = f'{settings_utils.get_parameter_from_settings("AIS_ADDRESS")}student/app/'
        if application.group.ou:
            url += f'course/{app_id}'
        else:
            url += f'event/{app_id}'
        msg = (f'Прикрепленный документ об оплате на участие в {group_type} "' + name + '" отклонен.\n'
               f'Комментарий от сотрудников центра: {message}.\n'
               f' Для просмотра заявки перейдите перейдите по ссылке: {url}\n'
               f'\nС уважением,\nкоманда АИС "Учебный Центр"')
        send_mail(
            subject,
            msg,
            None,
            # [application.profile.django_user.email, ],
            [settings_utils.get_parameter_from_settings('TEST_EMAIL'), ],
            fail_silently=False,
        )
        return f'Задача выполнена, письмо отправлено'

    wrapper()
