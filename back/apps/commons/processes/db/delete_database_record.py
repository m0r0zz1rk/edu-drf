from typing import Union

from django.apps import apps

from apps.commons.abc.main_processing import MainProcessing
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.validate import ValidateUtils
from apps.journal.consts.journal_modules import COMMON
from apps.journal.consts.journal_rec_statuses import SUCCESS, ERROR
from apps.journal.services.journal import JournalService


class DeleteDataBaseRecord(MainProcessing):
    """Процесс удаления записи из БД"""

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
                    if 'object_id' in self.process_data['object'].keys():
                        if ValidateUtils.validate_uuid(self.process_data['object']['object_id']):
                            return True
            return False
        except Exception:
            return ExceptionHandling.get_traceback()

    def _main_process(self):
        """
        Описание процесса удаления записи из БД
        :return:
        """
        self.model = apps.get_model(
            self.process_data['model_info']['app'],
            self.process_data['model_info']['model_name']
        )
        try:
            if 'id' in self.process_data['object']:
                self.model.objects.get(object_id=self.process_data['object']['id']).delete()
            elif 'object_id' in self.process_data['object']:
                self.model.objects.get(object_id=self.process_data['object']['object_id']).delete()
            else:
                pass
            return None
        except Exception:
            self._main_process_error(ExceptionHandling.get_traceback())
            self.process_completed = False

    def _main_process_error(self, traceback: str):
        """
        Фиксация ошибки при удалении записи из БД
        :param traceback: traceback возникшей в процессе ошибки
        :return:
        """
        JournalService().create_journal_rec(
            {
                'source': 'Процесс удаления записи из БД',
                'module': COMMON,
                'status': ERROR,
                'description': 'Произошла ошибка в процессе добавления/обновления записи в БД'
            },
            repr(self.process_data),
            traceback
        )

    def _process_success(self):
        """
        Фиксация сообщения об успешном удалении записи из БД
        :return:
        """
        JournalService().create_journal_rec(
            {
                'source': self.source,
                'module': self.module,
                'status': SUCCESS,
                'description': 'Запись успешно удалена'
            },
            repr(self.process_data),
            None
        )