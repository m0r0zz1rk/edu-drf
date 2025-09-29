import os
import celery

from celery.schedules import crontab
from django.apps import apps


class CeleryConfig:
    """Класс настройки celery"""

    app = None

    def __init__(self):
        """Инициализация"""
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_app.settings")

        self._init_celery()
        self._set_config_from_object()
        self._set_autodiscover_tasks()
        self._set_beat_schedule()

    def _init_celery(self):
        """Инициализация celery"""
        self.app = celery.Celery('web_app')

    def _set_config_from_object(self):
        """Установка параметров из django settings"""
        self.app.config_from_object('django.conf:settings', namespace='CELERY')

    def _set_autodiscover_tasks(self):
        """Настройка автоматического поиска задач"""
        self.app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

    def _set_beat_schedule(self):
        """Установка задач по расписанию"""
        self.app.conf.beat_schedule = {
            # 'check-registration-end': {
            #     'task': 'apps.celery_app.tasks.beat.check_registration_end.check_registration_end',
            #     'schedule': crontab(minute=0, hour=0)
            # },
            # 'check-start-event': {
            #     'task': 'apps.celery_app.tasks.beat.check_start_event.check_start_event',
            #     'schedule': crontab(minute=0, hour=0)
            # },
            # 'show-survey': {
            #     'task': 'apps.celery_app.tasks.beat.show_survey.show_survey',
            #     'schedule': crontab(minute=0, hour=0)
            # },
            'get-ad-and-old-data': {
                'task': 'apps.celery_app.tasks.beat.get_ad_and_old_data.get_ad_and_old_data',
                # 'schedule': crontab(minute=0, hour=1)
                'schedule': crontab(minute='*/2',)
            },
        }

    def get_instance(self) -> celery:
        """Получение инстанса Celery"""
        return self.app
