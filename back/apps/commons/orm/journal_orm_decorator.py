from apps.commons.models import BaseTable
from apps.commons.utils.django.exception import ExceptionHandling
from apps.journal.consts.journal_modules import ORM
from apps.journal.consts.journal_rec_statuses import SUCCESS, ERROR
from apps.journal.services.journal import JournalService

journal_service = JournalService()


def journal_orm_decorator(
        model: BaseTable,
        request_type: str,
        payload: str = '',
):
    """
    Декоратор для записи в журнал событий информации о ORM запросе к БД
    :param model: модель БД
    :param request_type: Тип SQL запроса
    :param payload: полезная нагрузка (для записи в журнале событий)
    :return:
    """
    def inner_decorator(function):
        def wrapper(*args, **kwargs):
            journal_info = dict(
                source='ORM',
                module=ORM,
                status=None,
                description=''
            )
            res = output = None
            try:
                res = function(*args, **kwargs)  # noqa
                # journal_info['status'] = SUCCESS
                # journal_info['description'] = f'Запрос на "{request_type}" к модели {model} выполнен успешно'
                # output = repr(res)
            except Exception as e:
                journal_info['status'] = ERROR
                journal_info['description'] = f'Запрос на "{request_type}" к модели {model} завершился ошибкой'
                output = ExceptionHandling.get_traceback()
            if journal_info['status'] == ERROR:
                journal_service.create_journal_rec(
                    data=journal_info,
                    payload=payload,
                    output=output
                )
            return res
        return wrapper
    return inner_decorator
