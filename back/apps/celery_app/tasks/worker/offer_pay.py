import uuid

from django.core.mail import send_mail

from apps.applications.services.base_application import base_application_service
from apps.celery_app.decorators.journal_celery_task import journal_celery_task
from apps.commons.utils.django.settings import settings_utils
from apps.edu.services.student_group import student_group_service
from web_app.init_celery import app


@app.task
def email_offer_pay(group_id: uuid):
    """
    Задача Celery на отправку обучающимся в группе писем с информацией об
    изменении статуса их заявки и необходимости произвести оплату за обучение
    :param group_id: object_id учебной группы
    :return:
    """

    @journal_celery_task(
        'Задача на отправку оферов  успешно выполнена',
        'Задача на отправку оферов завершилась ошибкой'
    )
    def wrapper():
        event_type, name, date_start, deadline = student_group_service.get_data_for_offer_pay_task(group_id)
        subject = 'АИС "Учебный Центр": Изменен статус Вашей заявки'
        msg = (f'Статус вашей заявки на участие в {event_type} "{name}" изменен на "Ждем оплату".\n'
               f'Оплата должна быть произведена не позднее {deadline.strftime("%d.%m.%Y")} года.'
               f' Для ознакомления с договором оферты и загрузки документа об оплате перейдите по ссылке: ')
        recipients = base_application_service.get_recipients_for_offer_pay(group_id)
        for recipient in recipients:
            msg += f'{recipient.get("url")}\nС уважением,\nкоманда АИС "Учебный Центр"'
            send_mail(
                subject,
                msg,
                None,
                # [recipient.get("email"), ],
                [settings_utils.get_parameter_from_settings('TEST_EMAIL'), ],
                fail_silently=False,
            )
        return f'Задача выполнена, отправлено {len(recipients)} писем'

    wrapper()
