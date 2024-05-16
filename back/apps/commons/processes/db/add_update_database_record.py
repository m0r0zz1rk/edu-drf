from typing import Union

from django.apps import apps
from django.contrib.auth.models import User

from apps.commons.abc.main_processing import MainProcessing
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.model import ModelUtils
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

    def _check_model_exist(self) -> bool:
        """
        Проверка на существующую модель в приложении
        :return: true - Модель существует, false - Модель не существует
        """
        if ((self.process_data['model_info']['app'] == 'django') &
                (self.process_data['model_info']['model_name'] == 'user')):
            return True
        model_exist = ModelUtils.is_model_exist_in_app(
            self.process_data['model_info']['app'],
            self.process_data['model_info']['model_name']
        )
        if model_exist is False or isinstance(model_exist, str):
            description = 'Указанная модель не найдена в приложении'
            output = None
            if isinstance(model_exist, str):
                description = 'Системная ошибка'
                output = model_exist
            JournalUtils().create_journal_rec(
                {
                    'source': 'Добавление/обновление записи',
                    'module': self.module,
                    'status': ERROR,
                    'description': description
                },
                f"Приложение: {self.process_data['model_info']['app']}, "
                f"Модель: {self.process_data['model_info']['model_name']}",
                output
            )
            return False
        return True

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
        if not self._check_model_exist():
            self.process_completed = False
            return None
        if ((self.process_data['model_info']['app'] == 'django') &
                (self.process_data['model_info']['model_name'] == 'user')):
            self.model = User
        else:
            self.model = apps.get_model(
                self.process_data['model_info']['app'],
                self.process_data['model_info']['model_name']
            )
        if self._validate_model_fields():
            try:
                if 'object_id' in self.process_data['object'].keys():
                    object_id = self.process_data['object']['object_id']
                    del self.process_data['object']['object_id']
                    self.model.objects.update_or_create(
                        object_id=object_id,
                        defaults=self.process_data['object']
                    )
                elif 'id' in self.process_data['object'].keys():
                    id = self.process_data['object']['id']
                    del self.process_data['object']['id']
                    self.model.objects.update_or_create(
                        id=id,
                        defaults=self.process_data['object']
                    )
                else:
                    self.model.objects.update_or_create(
                        **self.process_data['object']
                    )
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
