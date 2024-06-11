import abc

from apps.commons.utils.django.request import RequestUtils
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.services.journal import JournalService


class BaseProgramOperation(abc.ABC):
    """Базовый класс для работы с ДПП"""
    ju = JournalService()
    ru = RequestUtils()

    program_data = process_completed = error = None
    source = 'Базовое действие над ДПП'
    error_description = success_description = ''

    def __init__(self, program_data: dict, request=None):
        """
        Инициализация класса
        :param program_data: словарь с данными о ДПП
        :param request: Объект request
        """
        if request:
            self.source = self.ru.get_source_display_name(request)
        self.program_data = program_data
        if not self._validate_program_data():
            self._program_operation_error('Данные не прошли валидацию')
        else:
            self._main_action()

    def _program_operation_error(self, traceback: str):
        """
        Фиксация ошибки при выполнении действия над ДПП
        :param traceback: traceback возникшей в процессе ошибки
        :return:
        """
        self.ju.create_journal_rec(
            {
                'source': self.source,
                'module': EDU,
                'status': ERROR,
                'description': self.error_description
            },
            repr(self.program_data),
            traceback
        )

    def _program_operation_success(self):
        """
        Фиксация сообщения об успешном выполнении действия над ДПП
        :return:
        """
        self.ju.create_journal_rec(
            {
                'source': self.source,
                'module': EDU,
                'status': SUCCESS,
                'description': self.success_description
            },
            repr(self.program_data),
            None
        )

    @abc.abstractmethod
    def _validate_program_data(self) -> bool:
        """Валидация полученных данных"""
        pass

    @abc.abstractmethod
    def _main_action(self):
        """Выполнение действия над ДПП"""
        pass
