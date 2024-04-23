from apps.commons.utils.django.exception import ExceptionHandling
from apps.events.utils.events import EventsUtils
from apps.celery_app.tasks import email_for_event_change_status_task

from web_app.init_celery import app


@app.task
def check_events_app_dates_start_task():
    """Ежедневная проверка начала подачи заявок для мероприятий со статусом 'Опубликовано'"""
    try:
        events = EventsUtils.get_list_of_published_events()
        count = 0
        if events.count() > 0:
            for event in events:
                email_for_event_change_status_task(
                    event.object_id,
                    'PUBLISHED'
                )
                count += 1
        return f'Выполнено для {count} мероприятий'
    except Exception:
        return f'Ошибка: {ExceptionHandling.get_traceback()}'
