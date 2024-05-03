import uuid
from typing import Optional, Union

from django.apps import apps

from apps.commons.utils.django.exception import ExceptionHandling


class PayloadUtils:
    """Класс методов для работы с полезной нагрузки к записям журнала сообщений"""

    payload_model = None

    def __init__(self):
        """Инициализация класса - определение модели JournalPayload"""
        self.payload_model = apps.get_model('journal', 'JournalPayload')

    def is_payload_exist(self, journal_rec_id: uuid) -> bool:
        """
        Проверка наличия полезной нагрузки к записи журнала событий
        :param journal_rec_id: object_id записи журнала событий
        :return: true - полезная нагрузка есть, false - полезной нагрузки нет
        """
        return self.payload_model.objects.filter(journal_rec_id=journal_rec_id).exists()

    def get_payload(self, journal_rec_id: uuid) -> Optional[str]:
        """
        Получение полезной нагрузки к записи журнала событий
        :param journal_rec_id: object_id записи журнала событий
        :return: str - полезная нагрузка || None
        """
        if self.is_payload_exist(journal_rec_id):
            return self.payload_model.objects.get(journal_rec_id=journal_rec_id).payload
        return None

    def create_or_update_payload_rec(self, journal_rec_id: uuid, payload: str) -> Optional[str]:
        """
        Сохранение или обновление полезной нагрузки для записи журнала обработки
        :param journal_rec_id: object_id записи журнала обработки
        :param payload: полезная нагрузка в виде строки
        :return: None - полезная нагрузка сохранена, str - traceback ошибки при сохранении
        """
        try:
            if self.is_payload_exist(journal_rec_id):
                payload_rec = self.payload_model.objects.get(journal_rec_id=journal_rec_id)
                payload_rec.payload = payload
                payload_rec.save()
            else:
                self.payload_model.objects.create(
                    journal_rec_id=journal_rec_id,
                    payload=payload
                )
            return None
        except Exception:
            return ExceptionHandling.get_traceback()
