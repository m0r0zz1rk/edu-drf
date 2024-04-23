import uuid

from django.conf import settings
from django.core.mail import send_mail

from apps.authen.utils.profile import ProfileUtils
from apps.celery_app.utils import UserEventEmailsUtils
from apps.commons.consts.events.event_statuses import EVENT_STATUSES
from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import CELERY_APP
from apps.commons.utils.django.exception import ExceptionHandling
from apps.events.utils.events import EventsUtils
from apps.journals.writer.journal_writer import JournalWriter
from web_app.init_celery import app


@app.task
def email_for_event_change_status_task(event_id: uuid, new_status: EVENT_STATUSES):
    """
        Проверка на изменение статуса мероприятия,
        в случае изменения на ОПУБЛИКОВАНО, В ПРОЦЕССЕ - отправить письмо пользователям
        с соответствующими ролями
    """
    try:
        eu = EventsUtils()
        event = EventsUtils.get_event_by_object_id(event_id)
        subject = text = ''
        count = 0
        recipient_list = []
        match new_status:
            case 'PUBLISHED':
                if event.check_date_in_app_dates():
                    subject = 'АИС "Мероприятия ИОХК": Опубликовано новое мероприятие'
                    text = (f'<br>Приглашаем Вас принять участие в мероприятии.'
                            f'<br>Наименование: <b>{event.name}</b>'
                            f'<br>Тип мероприятия: <b>{event.event_type.name}</b>'
                            f'<br>Сроки подачи заявок: <b>{event.app_date_start.strftime('%d.%m.%Y')}-'
                            f'{event.app_date_end.strftime('%d.%m.%Y')}</b>'
                            f'<br>Сроки проведения: <b>{event.date_start.strftime('%d.%m.%Y')}-'
                            f'{event.date_end.strftime('%d.%m.%Y')}</b>')

        if len(subject) > 0:
            if new_status == 'PUBLISHED':
                for email in eu.get_list_of_potential_user_emails(event.object_id):
                    if not UserEventEmailsUtils.check_event_published(
                        ProfileUtils.get_user_id_by_email(email),
                        event_id
                    ):
                        UserEventEmailsUtils.create_rec_event(
                            ProfileUtils.get_user_id_by_email(email),
                            event_id,
                            'PUBLISHED'
                        )
                        profile = ProfileUtils.get_profile_by_user_email(email)
                        if profile is not None:
                            appeal = 'Уважаемая'
                            if profile.sex:
                                appeal = 'Уважаемый'
                            message = f'{appeal} {profile.get_display_name()}!\n{text}'
                            send_mail(
                                subject,
                                None,
                                settings.EMAIL_HOST_USER,
                                [email,],
                                fail_silently=False,
                                html_message=message
                            )
                            count += 1
        return f'Выполнено, отправлено сообщений: {count}'
    except Exception:
        journal = JournalWriter(CELERY_APP)
        journal.write(
            'Celery',
            ERROR,
            f'Ошибка при отправки сообщений в связи с изменением статуса мероприятия: '
            f'{ExceptionHandling.get_traceback()}'
        )
        return f'Ошибка: {ExceptionHandling.get_traceback()}'
