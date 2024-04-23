from django.db import models

from apps.commons.models import BaseTable
from apps.commons.utils.data_types.date import DateUtils
from apps.journal.models.journal import Journal


class JournalOutput(BaseTable):
    """Модель результата/выходных данных к записи журнала событий"""
    journal_rec = models.OneToOneField(
        Journal,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Запись журнала событий'
    )
    output = models.TextField(
        max_length=100000,
        null=True,
        blank=True,
        default=None,
        verbose_name='Результат/Выходные данные'
    )

    def __str__(self):
        return (f'Результат/Выходные данные к записи журнала {self.journal_rec.object_id} от '
                f'{DateUtils.convert_date_to_str(self.journal_rec.date_create)}')

    class Meta:
        verbose_name = 'Результат/Выходные данные к записи журнала событий'
        verbose_name_plural = 'Результаты/Выходные данные к записям журнала событий'
