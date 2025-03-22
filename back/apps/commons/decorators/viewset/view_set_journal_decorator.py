from django.contrib.auth.models import AnonymousUser

from apps.commons.utils.django.exception import exception_handling
from apps.commons.utils.django.response import response_utils
from apps.journal.consts.journal_modules import JOURNAL_MODULES
from apps.journal.consts.journal_rec_statuses import SUCCESS, ERROR
from apps.journal.services.journal import journal_service


def view_set_journal_decorator(module: JOURNAL_MODULES, success_description: str, error_description: str):
    """
    Декоратор для фиксации использования эндпоинтов в журнале событий
    :param module: Модуль системы
    :param success_description: Описание успешной операции для фиксации в журнале
    :param error_description: Описание ошибки для фиксации в журнале
    :return:
    """
    def wrapper(function):
        def inner_wrapper(*args, **kwargs):
            payload = {}
            if kwargs:
                payload = kwargs
            if args:
                payload['args'] = args

            source = 'Анонимный пользователь'
            request_object = args[1]
            if not isinstance(request_object.user, AnonymousUser):
                source = 'Зарегистрированный пользователь '
                if request_object.user.last_name:
                    source = f'{request_object.user.last_name} '
                if request_object.user.first_name:
                    source += request_object.user.first_name

            try:
                res = function(*args, **kwargs)
                journal_service.create_journal_rec(
                    {
                        'source': source,
                        'module': module,
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
                        'source': source,
                        'module': module,
                        'status': ERROR,
                        'description': error_description
                    },
                    repr(payload),
                    exception_handling.get_traceback()
                )
                return response_utils.bad_request_no_data()
        return inner_wrapper
    return wrapper
