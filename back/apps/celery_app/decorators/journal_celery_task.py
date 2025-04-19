from sre_constants import SUCCESS

from apps.commons.utils.django.exception import exception_handling
from apps.journal.consts.journal_modules import CELERY
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import journal_service
from web_app.init_celery import app


def logger_task(function):
    """
    Декоратор для фиксации выполнения задачи Celery в журнале
    :param function: Задача Celery
    :return:
    """
    task_name = function.__name__

    def wrapper(*args, **kwargs):
        payload = {}
        if kwargs:
            payload = kwargs
        if args:
            payload['args'] = args
        try:
            res = function(*args, **kwargs)
            journal_service.create_journal_rec(
                {
                    'source': 'Брокер CELERY',
                    'module': CELERY,
                    'status': SUCCESS,
                    'description': f'Задача {task_name} успешно выполнена'
                },
                repr(payload),
                repr(res)
            )
            return res
        except Exception:
            journal_service.create_journal_rec(
                {
                    'source': 'Брокер CELERY',
                    'module': CELERY,
                    'status': ERROR,
                    'description': f'Задача {task_name} завершилась ошибкой'
                },
                repr(payload),
                exception_handling.get_traceback()
            )

    app.task(bind=True, name=task_name)(wrapper)
    return wrapper


def journal_celery_task(success_description: str, error_description: str):
    """
    Декоратор для фиксации выполнения задач Celery в журнале
    :param success_description: Описание успешного выполнения задачи для фиксации в журнале
    :param error_description: Описание ошибки при выполнении задачи для фиксации в журнале
    :return:
    """
    def wrapper(function):
        def inner_wrapper(*args, **kwargs):
            payload = {}
            if kwargs:
                payload = kwargs
            if args:
                payload['args'] = args
            try:
                res = function(*args, **kwargs)
                journal_service.create_journal_rec(
                    {
                        'source': 'Брокер CELERY',
                        'module': CELERY,
                        'status': SUCCESS,
                        'description': success_description
                    },
                    repr(payload),
                    repr(res)
                )
                return res
            except Exception:
                journal_service.create_journal_rec(
                    {
                        'source': 'Брокер CELERY',
                        'module': CELERY,
                        'status': ERROR,
                        'description': error_description
                    },
                    repr(payload),
                    exception_handling.get_traceback()
                )
        return inner_wrapper
    return wrapper
