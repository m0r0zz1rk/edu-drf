# import os
# import celery
#
# from celery.schedules import crontab
# from django.apps import apps
#
#
# class CeleryConfig:
#     """Класс настройки celery"""
#
#     app = None
#
#     def __init__(self):
#         """Инициализация"""
#         os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_app.settings")
#
#         self._init_celery()
#         self._set_config_from_object()
#         self._set_autodiscover_tasks()
#         self._set_beat_schedule()
#
#     def _init_celery(self):
#         """Инициализация celery"""
#         self.app = celery.Celery('webapp')
#
#     def _set_config_from_object(self):
#         """Установка параметров из django settings"""
#         self.app.config_from_object('django.conf:settings', namespace='CELERY')
#
#     def _set_autodiscover_tasks(self):
#         """Настройка автоматического поиска задач"""
#         self.app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
#
#     def _set_beat_schedule(self):
#         """Установка задач по расписанию"""
#         self.app.conf.beat_schedule = {
#             'check-app-dates': {
#                 'task': 'apps.celery_app.tasks.events.check_events_app_dates_start.check_events_app_dates_start_task',
#                 'schedule': crontab(minute=0, hour=0)
#             },
#             'check-start-tomorrow': {
#                 'task': 'apps.celery_app.tasks.events.check_start_tomorrow.check_start_tomorrow_task',
#                 'schedule': crontab(minute=0, hour=0)
#             },
#             'check-start-today': {
#                 'task': 'apps.celery_app.tasks.events.check_start_today.check_start_today_task',
#                 'schedule': crontab(minute=0, hour=0)
#             },
#             'check-event-status': {
#                 'task': 'apps.celery_app.tasks.events.change_event_status.change_event_status_task',
#                 'schedule': crontab(minute=0, hour=0)
#             },
#         }
#
#     def get_instance(self) -> celery:
#         """Получение инстанса Celery"""
#         return self.app
