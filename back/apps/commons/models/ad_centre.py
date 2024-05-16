from django.db import models

from apps.commons.models import BaseTable


class AdCentre(BaseTable):
    """Модель подразделений уровня Центр из Active Directory COKO"""
    display_name = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name='Наименование подразделения'
    )
    object_guid = models.CharField(
        max_length=38,
        null=False,
        blank=False,
        unique=True,
        verbose_name='ObjectGUID подразделения из AD'
    )

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = 'Подразделение-центр из AD'
        verbose_name_plural = 'Подразделения-центры из AD'
