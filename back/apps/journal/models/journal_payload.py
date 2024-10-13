from django.db import models

from apps.commons.models import BaseTable
from apps.commons.utils.data_types.date import DateUtils
from apps.journal.models.journal import Journal


class JournalPayload(BaseTable):
    """Модель данных о полезной нагрузке к записи журнала событий"""
    journal_rec = models.OneToOneField(
        Journal,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Запись журнала событий'
    )
    payload = models.TextField(
        max_length=100000,
        blank=True,
        default=None,
        verbose_name='Полезная нагрузка'
    )

    def __str__(self):
        return (f'Полезная нагрузка к записи журнала {self.journal_rec.object_id} от '
                f'{DateUtils.convert_date_to_str(self.journal_rec.date_create)}')

    class Meta:
        verbose_name = 'Полезная нагрузка к записи журнала событий'
        verbose_name_plural = 'Полезные нагрузки к записям журнала событий'
