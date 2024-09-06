from apps.commons.utils.django.response import ResponseUtils
from apps.journal.consts.journal_modules import JOURNAL_MODULES
from apps.journal.consts.journal_rec_statuses import JOURNAL_REC_STATUSES
from apps.journal.services.journal import JournalService


class JournalRequestBuilder:
    """Класс строителя объекта для класса JournalRequest"""

    _module = _status = None
    _payload = _output = _description = _response_message = ''

    def set_module(self, module: JOURNAL_MODULES):
        """Установить модуль журнала"""
        self._module = module
        return self

    def set_status(self, status: JOURNAL_REC_STATUSES):
        """Устноавить статус сообщения журнала"""
        self._status = status
        return self

    def set_payload(self, payload: str):
        """Установить полезную нагрузку для записи журнала"""
        self._payload = payload
        return self

    def set_output(self, output: str):
        """Установить выходные данные для записи журнала"""
        self._output = output
        return self

    def set_description(self, description: str):
        """Установить описание для записи журнала"""
        self._description = description
        return self

    def set_response_message(self, response_message: str):
        """Установить сообщение в response"""
        self._response_message = response_message
        return self


class JournalRequest:
    """Класс для добавления записи в журнал событий и отправки ответа response"""

    _module = _status = None
    _payload = _output = _description = _response_message = ''
    _journal_service = JournalService()
    _response_utils = ResponseUtils()

    def __init__(self, builder: JournalRequestBuilder):
        """Установка значений переменных из класса строителя и вызов метода добавления записи в журнал"""
        for var in vars(builder):
            setattr(self, var, getattr(builder, var))
        self.add_journal_rec()

    def add_journal_rec(self):
        """Добавление записи в журнал"""
        self._journal_service.create_journal_rec(
            {
                'source': 'Внешний запрос',
                'module': self._module,
                'status': self._status,
                'description': self._description
            },
            self._payload,
            self._output
        )

    def create_response(self):
        """Создание объекта response"""
        return self._response_utils.bad_request_response(self._response_message)