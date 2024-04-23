import uuid

from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail

from apps.commons.consts.apps.app_statuses import APP_STATUSES
from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import CELERY_APP
from apps.commons.utils.django.exception import ExceptionHandling
from apps.journals.writer.journal_writer import JournalWriter
from web_app.init_celery import app

apps_model = apps.get_model('applications', 'Apps')

@app.task
def app_change_status_task(app_id: uuid, status: APP_STATUSES, message=None):
    """Отправка сообщения об изменении статуса заявки"""
    try:
        appl = apps_model.objects.get(object_id=app_id)
        match status:
            case 'ACCEPTED':
                subject = 'АИС "Мероприятия ИОХК": Заявка успешно принята'
                text = (f'<br>Ваша заявка на участие в мероприятии: {appl.event.event_type.name} <b>"{appl.event.name}"</b> '
                        f'успешно принята.'
                        f'<br>Напоминаем, что мероприятие будет проходить в период с '
                        f'{appl.event.date_start.strftime('%d.%m.%Y')} по '
                        f'{appl.event.date_end.strftime('%d.%m.%Y')} включительно')

            case 'REJECTED':
                subject = 'АИС "Мероприятия ИОХК": Заявка отклонена'
                text = (f'<br>Ваша заявка на участие в мероприятии: {appl.event.event_type.name} <b>"{appl.event.name}"</b> '
                        f'была отклонена.<br>Комментарий организатора: '
                        f'<br><b>{message}</b><br>Вы можете устранить замечания, и вновь подать заявку на '
                        f'участие до {appl.event.app_date_end.strftime('%d.%m.%Y')} включительно.')

            case 'COMPLETED':
                subject = 'АИС "Мероприятия ИОХК": Мероприятие завершено'
                text = (f'<br>Мероприятие: {appl.event.event_type.name} <b>"{appl.event.name}"</b> '
                        f'успешно завершено.<br> Ознакомиться с результатом Вы можете в Личном кабинете '
                        f'АИС "Мероприятия ИОХК", перейдя к соответствующей заявке')

            case _:
                return 'Некорректный статус заявки'
        profile = appl.profile
        appeal = 'Уважаемая'
        if profile.sex:
            appeal = 'Уважаемый'
        message = f'{appeal} {profile.get_display_name()}!\n{text}'
        send_mail(
            subject,
            None,
            settings.EMAIL_HOST_USER,
            [profile.django_user.email, ],
            fail_silently=False,
            html_message=message
        )
        return 'Сообщение о смене статуса заявки успешно отправлено'
    except Exception:
        journal = JournalWriter(CELERY_APP)
        journal.write(
            'Celery',
            ERROR,
            f'Ошибка при отправки сообщений об изменении статуса заявки: '
            f'{ExceptionHandling.get_traceback()}'
        )
        return f'Ошибка: {ExceptionHandling.get_traceback()}'
