import uuid
from typing import Optional

from apps.commons.utils.django.exception import ExceptionHandling
from apps.journal.selectors.journal_output import journal_output_model


class OutputService:
    """Класс методов для работы с выходными данными к записи журнала событий"""

    @staticmethod
    def is_output_exist(journal_rec_id: uuid) -> bool:
        """
        Проверка наличия выходных данных к записи журнала событий
        :param journal_rec_id: object_id записи журнала событий
        :return: true - выходные данные есть, false - выходных данных нет
        """

        return journal_output_model.objects.filter(journal_rec_id=journal_rec_id).exists()

    def get_output(self, journal_rec_id: uuid) -> Optional[str]:
        """
        Получение выходных данных к записи журнала событий
        :param journal_rec_id: object_id записи журнала событий
        :return: str - выходные данные || None
        """
        if self.is_output_exist(journal_rec_id):
            return journal_output_model.objects.get(journal_rec_id=journal_rec_id).output
        return None

    def create_or_update_output_rec(self, journal_rec_id: uuid, output: str) -> Optional[str]:
        """
        Сохранение или обновление выходных данных для записи журнала обработки
        :param journal_rec_id: object_id записи журнала обработки
        :param output: выходные данные в виде строки
        :return: None - выходные данные сохранены, str - traceback ошибки при сохранении
        """
        try:
            if self.is_output_exist(journal_rec_id):
                output_rec = journal_output_model.objects.get(journal_rec_id=journal_rec_id)
                output_rec.output = output
                output_rec.save()
            else:
                journal_output_model.objects.create(
                    journal_rec_id=journal_rec_id,
                    output=output
                )
            return None
        except Exception:
            return ExceptionHandling.get_traceback()


output_service = OutputService()
