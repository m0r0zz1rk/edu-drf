import datetime

from apps.commons.consts.events.event_statuses import PUBLISHED, ONGOING, COMPLETED
from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import CELERY_APP
from apps.commons.utils.django.exception import ExceptionHandling
from apps.events.utils.events import EventsUtils
from apps.journals.writer.journal_writer import JournalWriter
from web_app.init_celery import app


@app.task
def change_event_status_task():
    """Изменение статусов мероприятий на 'В процессе' и 'Завершено'"""
    try:
        count = 0
        events = EventsUtils.get_all_events()
        for event in events:
            if event.event_status == PUBLISHED and \
                    event.date_start <= datetime.date.today() <= event.date_end:
                event.event_status = ONGOING
                event.save()
                count += 1
            if event.event_status == ONGOING and \
                    event.date_end < datetime.date.today():
                event.event_status = COMPLETED
                event.save()
                count += 1
        return f'Выполнено, количество измененных статусов мероприятий: {count}'
    except Exception:
        journal = JournalWriter(CELERY_APP)
        journal.write(
            'Celery',
            ERROR,
            f'Ошибка при изменении статуса мероприятия: '
            f'{ExceptionHandling.get_traceback()}'
        )
        return f'Ошибка: {ExceptionHandling.get_traceback()}'
