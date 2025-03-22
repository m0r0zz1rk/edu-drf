from apps.commons.utils.django.exception import exception_handling
from apps.journal.consts.journal_modules import COMMON
from apps.journal.consts.journal_rec_statuses import SUCCESS, ERROR
from apps.journal.services.journal import journal_service


def ldap_utils_journal_decorator(success_description: str, error_description: str):
    """
    Декоратор для фиксации использования ldap_utils в журнале событий
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

            try:
                res = function(*args, **kwargs)
                journal_service.create_journal_rec(
                    {
                        'source': 'Active Directory',
                        'module': COMMON,
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
                        'source': 'Active Directory',
                        'module': COMMON,
                        'status': ERROR,
                        'description': error_description
                    },
                    repr(payload),
                    exception_handling.get_traceback()
                )
        return inner_wrapper
    return wrapper
