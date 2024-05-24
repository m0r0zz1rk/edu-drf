from abc import ABC, abstractmethod

from apps.commons.utils.django.model import ModelUtils
from apps.commons.utils.django.request import RequestUtils
from apps.journal.consts.journal_modules import DOCS
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.utils.journal_utils import JournalUtils


class BaseDocOperation(ABC):
    """Базовый класс для действий с документами"""

    ju = JournalUtils()
    document_data = model = request = success_message = error_message = doc_id = None
    error = process_completed = False

    def _doc_operation_error(self, traceback: str):
        """
        Фиксация ошибки при выполнении действия над документом
        :param traceback: traceback возникшей в процессе ошибки
        :return:
        """
        self.ju.create_journal_rec(
            {
                'source': 'Действие над документом',
                'module': DOCS,
                'status': ERROR,
                'description': 'Произошла ошибка в процессе выполнения действия с документом'
            },
            repr(self.document_data),
            traceback
        )

    def _doc_operation_success(self):
        """
        Фиксация сообщения об успешном ыполнении действия над документом
        :param traceback: traceback возникшей в процессе ошибки
        :return:
        """
        self.ju.create_journal_rec(
            {
                'source': 'Действие над документом',
                'module': DOCS,
                'status': SUCCESS,
                'description': self.success_message
            },
            repr(self.document_data),
            None
        )

    def _check_doc_model_exists(self):
        """
        Проверка на существующую модель в приложении docs
        :return:
        """
        result = ModelUtils.is_model_exist_in_app(
            'docs',
            self.model
        )
        return isinstance(result, bool) and result

    def __init__(self, document_data: dict, model: str, request=None):
        """
        Инициализация класса
        :param document_data: словарь с данными по добавляемому/редактируемому документу
        :param model: Наименование модели приложения docs
        :param request: Объект request
        """
        self.document_data = document_data
        self.model = model
        if isinstance(self._check_doc_model_exists(), str):
            self._doc_operation_error(self._check_doc_model_exists())
            self.error = True
        elif not self._check_doc_model_exists():
            self._doc_operation_error('Указанная модель не найдена модуле документов')
            self.error = True
        else:
            self.request = request
            self._process()
            if self.process_completed:
                self._doc_operation_success()
            else:
                self._doc_operation_error(self.error_message)

    def _process(self):
        """Процесс работы с документом"""
        source = 'Система'
        module = DOCS
        if self.request is not None:
            source = RequestUtils.get_source_display_name(self.request)
        process_data = {
            'source': source,
            'module': module,
            'process_data': {
                'model_info': {
                    'app': 'docs',
                    'model_name': self.model
                },
                'document_data': self.document_data
            }
        }
        self.action(process_data)

    @abstractmethod
    def action(self, process_data: dict):
        """Действие над документом"""
        pass
