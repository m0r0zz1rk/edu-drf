from django.db import models

from apps.commons.models import BaseTable
from apps.commons.utils.data_types.date import DateUtils
from apps.journal.consts.journal_modules import JOURNAL_MODULES, COMMON
from apps.journal.consts.journal_rec_statuses import JOURNAL_REC_STATUSES, NO_RESULT


class Journal(BaseTable):
    """Модель журнала событий АИС"""
    source = models.CharField(
        max_length=500,
        null=False,
        blank=True,
        default='',
        verbose_name='Источник события'
    )
    module = models.CharField(
        max_length=35,
        choices=JOURNAL_MODULES,
        default=COMMON,
        blank=False,
        null=False,
        verbose_name='Модуль АИС'
    )
    status = models.CharField(
        max_length=15,
        choices=JOURNAL_REC_STATUSES,
        default=NO_RESULT,
        blank=False,
        null=False,
        verbose_name='Статус события'
    )
    description = models.TextField(
        max_length=150000,
        null=False,
        blank=True,
        default='',
        verbose_name='Краткое описание результата события'
    )

    def __str__(self):
        return f'Событий {self.object_id} от {DateUtils.convert_date_to_str(self.date_create)}'

    class Meta:
        verbose_name = 'Запись журнала событий'
        verbose_name_plural = 'Записи журнала событий'
