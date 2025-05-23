from .base import *
from kombu.serialization import registry

# Настройки инстанса Celery
CELERY_IMPORTS = ("apps.celery_app.tasks", )
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = env.str('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json', 'application/text', 'web_app/json']

# Разрешенные типы контента (content-type)
registry.enable('json')
registry.enable('application/text')
registry.enable('web_app/json')

# Переменные для задач
STUDENT_GROUP_STATEMENT_DAYS = env.int('STUDENT_GROUP_STATEMENT_DAYS', 10)
