from functools import wraps

from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.response import ResponseUtils
from apps.journal.consts.journal_modules import JOURNAL_MODULES
from apps.journal.consts.journal_rec_statuses import JOURNAL_REC_STATUSES
from apps.journal.exceptions.api_process_error import APIProcessError
from apps.journal.services.journal import JournalService

response_utils = ResponseUtils()
journal_service = JournalService()
exception_handling = ExceptionHandling()


def journal_api(
        source: str,
        module: JOURNAL_MODULES,
        status: JOURNAL_REC_STATUSES,
        description: str,
        error_text: str
):
    """Декоратор для внесения ошибок в журнал событий в случае их возникновения при работе с endpoint"""
    def inner_decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)
            except APIProcessError:
                journal_service.create_journal_rec(
                    {
                        'source': source,
                        'module': module,
                        'status': status,
                        'description': description
                    },
                    '-',
                    ExceptionHandling.get_traceback()
                )
                return response_utils.bad_request_response(error_text)
        return wrapper
    return inner_decorator
