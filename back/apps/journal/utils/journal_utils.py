import uuid

from django.apps import apps

from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.validate import ValidateUtils
from apps.journal.consts.journal_modules import COMMON
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.utils.output_utils import OutputUtils
from apps.journal.utils.payload_utils import PayloadUtils


class JournalUtils:
    """Класс методов для работы с журналом событий"""

    fields = []
    journal_model = None

    def __init__(self):
        """Инициализация класса - получение списка полей модели для валидации данных"""
        self.journal_model = apps.get_model('journal', 'Journal')
        self.fields = [field.name for field in self.journal_model._meta.get_fields()]

    def is_journal_rec_exist(self, rec_id: uuid) -> bool:
        """
        Проверка на наличие записи в журнале обработки
        :param rec_id: object_id записи
        :return: true - запись существует, false - запись не существует
        """
        return self.journal_model.objects.filter(object_id=rec_id).exists()

    def get_journal_size(self) -> int:
        """
        Получение текущего размера журнала
        :return: количество записей в таблице Journal
        """
        return self.journal_model.objects.count()

    def create_journal_rec(self, data: dict, payload: str = None, output: str = None):
        """
        Внесение новой записи в журнал событий
        :param data: полученные данные для модели Journal
        :param payload: полезная нагрузка для записи в журнал событий
        :param output: выходные данные для записи в журнал событий
        :return:
        """
        if ValidateUtils.validate_data(self.fields, data):
            payload_utils = PayloadUtils()
            output_utils = OutputUtils()
            try:
                new_rec = self.journal_model(**data)
                new_rec.save()
                if payload is not None or output is not None:
                    if self.is_journal_rec_exist(new_rec.object_id):
                        description = data['description']
                        if payload is not None:
                            payload_save_process = payload_utils.create_or_update_payload_rec(
                                new_rec.object_id,
                                payload
                            )
                            if payload_save_process is not None:
                                description += (f' (Ошибка при сохранении полезной '
                                                f'нагрузки:{payload_save_process[:5000]})')
                        if output is not None:
                            output_save_process = output_utils.create_or_update_output_rec(
                                new_rec.object_id,
                                output
                            )
                            if output_save_process is not None:
                                description += (f' (Ошибка при сохранении '
                                                f'выходных данных:{output_save_process[:5000]})')
                        new_rec.description = description
                        new_rec.save()
            except Exception:
                error_rec = self.journal_model(
                    source='Процесс создания записи в журнале событий',
                    module=COMMON,
                    status=ERROR,
                    description=''
                )
                error_rec.save()
                if self.is_journal_rec_exist(error_rec.object_id):
                    description = 'Произошла ошибка при внесении записи в журнал событий'
                    payload_save_process = payload_utils.create_or_update_payload_rec(
                        error_rec.object_id,
                        repr(data)
                    )
                    if payload_save_process is not None:
                        description += f' (Ошибка при сохранении полезной нагрузки:{payload_save_process[:5000]})'
                    output_save_process = output_utils.create_or_update_output_rec(
                        error_rec.object_id,
                        ExceptionHandling.get_traceback()
                    )
                    if output_save_process is not None:
                        description += f' (Ошибка при сохранении выходных данных:{output_save_process[:5000]})'
                    error_rec.description = description
                    error_rec.save()

    def journal_older_delete(self):
        """Удаление самой старой записи в журнале событий"""
        self.journal_model.objects.order_by('date_create').first().delete()
