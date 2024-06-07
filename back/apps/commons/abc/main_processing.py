from abc import ABC, abstractmethod
from typing import Union

from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.validate import ValidateUtils
from apps.journal.consts.journal_modules import JOURNAL_MODULES, COMMON
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.utils.journal_utils import JournalUtils


class MainProcessing(ABC):
    """Абстрактный класс выполнения процесса внутри АИС"""

    required_data_keys = [
        'source',
        'module',
        'process_data'
    ]
    source = module = process_data = None
    process_completed = True
    ju = JournalUtils()

    def __init__(self, income_data: dict):
        """Инициализация класса"""
        if self._validate_income_data(income_data):
            self._set_data(income_data)
            self._processing()
        else:
            self.ju.create_journal_rec(
                {
                    'source': 'Процесс обработки информации',
                    'module': COMMON,
                    'status': ERROR,
                    'description': 'Ошибки при инициализации процесса обработки - данные не прошли валидацию'
                },
                repr(income_data),
                None
            )
            self.process_completed = False

    def _validate_income_data(self, income_data) -> bool:
        """
        Валидация полученных данных
        :return: true - данные валидны, false - данные не валидны
        """
        if ValidateUtils.validate_data(
                self.required_data_keys,
                income_data
        ):
            if income_data['module'] in dict(JOURNAL_MODULES):
                return True
        return False

    def _set_data(self, income_data: dict):
        """Установка полученных данных в атрибут класса"""
        for attr in self.required_data_keys:
            setattr(self, attr, income_data[attr])

    @abstractmethod
    def _validate_process_data(self) -> Union[bool, str]:
        """
        Валидация данных для процесса обработки
        :return: true - данные валидны, false - данные не валидны, str - traceback
        """
        pass

    def _validate_process_data_error(self, traceback: str = None):
        """Создание записи в журнале обработки об ошибке валидации данных для процесса обработки"""
        journal_rec = {
            'data': {
                'source': self.source,
                'module': self.module,
                'status': ERROR,
                'description': 'Ошибка валидации данных для процесса обработки'
            },
            'payload': repr(self.process_data)
        }
        if traceback is not None:
            journal_rec.output = traceback
        self.ju.create_journal_rec(**journal_rec)

    @abstractmethod
    def _main_process(self):
        """Процесс обработки информации"""
        pass

    @abstractmethod
    def _process_success(self):
        """Метод, выполняющийся после успешного окончания процесса обработки"""
        pass

    def _process_error(self, traceback: str):
        """Создание записи об ошибки в процессе обработки в журнале событий"""
        self.ju.create_journal_rec(
            {
                'source': self.source,
                'module': self.module,
                'status': ERROR,
                'description': 'Ошибка во время процесса обработки'
            },
            repr(self.process_data),
            traceback
        )

    def _processing(self):
        """Выполнение процесса"""
        try:
            valid = self._validate_process_data()
            if valid is True:
                self._main_process()
                if self.process_completed:
                    self._process_success()
            else:
                if valid is False:
                    self._validate_process_data_error()
                else:
                    self._validate_process_data_error(valid)
                self.process_completed = False
        except Exception:
            self._process_error(ExceptionHandling.get_traceback())
            self.process_completed = False
