from typing import Union

from django.apps import apps

from apps.commons.abc.main_processing import MainProcessing
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.validate import ValidateUtils
from apps.journal.consts.journal_modules import COMMON
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.utils.journal_utils import JournalUtils


class AddUpdateDataBaseRecord(MainProcessing):
    """Процесс добавления/обновления записи в БД"""

    model = None
    fields_validated = True

    def _validate_process_data(self) -> Union[bool, str]:
        """
        Валидация данных для процесса обработки
        :return: true - данные валидны, false - данные не валидны, str - traceback
        """
        try:
            if 'model_info' in self.process_data.keys():
                counter = 0
                for info in ['app', 'model_name']:
                    if info in self.process_data['model_info'].keys():
                        counter += 1
                if counter == 2:
                    if 'object' in self.process_data.keys():
                        if isinstance(self.process_data['object'], dict):
                            return True
            return False
        except Exception:
            return ExceptionHandling.get_traceback()

    def _validate_model_fields(self) -> bool:
        """
        Валидация полей модели и полей, полученных из данных для процесса обработки
        :return:
        """
        model_fields = [field.name for field in self.model._meta.get_fields()]
        if ValidateUtils.validate_data(model_fields, self.process_data['object']):
            return True
        return False

    def _validate_model_fields_error(self):
        """
        Фиксация ошибки валидации полей модели в журнале событий
        :return:
        """
        JournalUtils().create_journal_rec(
            {
                'source': self.source,
                'module': self.module,
                'status': ERROR,
                'description': 'Не пройдена валидация полей модели'
            },
            repr(self.process_data),
            None
        )

    def _main_process_error(self, traceback: str):
        """
        Фиксация ошибки при создании/обновлении записи в БД
        :param traceback: traceback возникшей в процессе ошибки
        :return:
        """
        JournalUtils().create_journal_rec(
            {
                'source': 'Процесс добавления/обновления записи в БД',
                'module': COMMON,
                'status': ERROR,
                'description': 'Произошла ошибка в процессе добавления/обновления записи в БД'
            },
            repr(self.process_data),
            traceback
        )

    def _main_process(self):
        """
        Описание процесса добавления/обновления записи в БД
        :return:
        """
        self.model = apps.get_model(
            self.process_data['model_info']['app'],
            self.process_data['model_info']['model_name']
        )
        if self._validate_model_fields():
            try:
                self.model.objects.update_or_create(**self.process_data['object'])
                return None
            except Exception:
                self._main_process_error(ExceptionHandling.get_traceback())
                self.process_completed = False
        else:
            self._validate_model_fields_error()
            self.process_completed = False

    def _process_success(self):
        """
        Фиксация сообщения об успешном добавлении/обновлении записи в БД
        :return:
        """
        JournalUtils().create_journal_rec(
            {
                'source': self.source,
                'module': self.module,
                'status': SUCCESS,
                'description': 'Запись успешно добавлена/обновлена'
            },
            repr(self.process_data),
            None
        )
