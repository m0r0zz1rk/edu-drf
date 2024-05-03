from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.commons.models import BaseTable
from apps.commons.utils.data_types.date import DateUtils
from apps.commons.utils.django.settings import SettingsUtils
from apps.journal.consts.journal_modules import JOURNAL_MODULES, COMMON
from apps.journal.consts.journal_rec_statuses import JOURNAL_REC_STATUSES, NO_RESULT
from apps.journal.utils.journal_utils import JournalUtils


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


@receiver(post_save, sender=Journal)
def journal_house_keeping(sender, **kwargs):
    """Удаление записей из журнала событий при превышении размера журнала"""
    journal_max = SettingsUtils().get_parameter_from_settings('JOURNAL_MAX_LENGTH')
    if journal_max is None:
        journal_max = 250000
    ju = JournalUtils()
    if ju.get_journal_size() > journal_max:
        ju.journal_older_delete()
