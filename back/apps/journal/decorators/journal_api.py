from functools import wraps

from apps.commons.services.journal_request import JournalRequestBuilder, JournalRequest
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
        module: JOURNAL_MODULES,
        status: JOURNAL_REC_STATUSES,
        description: str,
        error_text: str
):
    """Декоратор для внесения ошибок в журнал событий в случае их возникновения при работе с endpoint"""
    _journal_request_builder = JournalRequestBuilder()

    def inner_decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)
            except APIProcessError:
                journal_request = JournalRequest(
                    _journal_request_builder
                    .set_module(module)
                    .set_status(status)
                    .set_description(description)
                    .set_payload('-')
                    .set_output(ExceptionHandling.get_traceback())
                    .set_response_message(error_text)
                )
                return journal_request.create_response()
        return wrapper
    return inner_decorator
