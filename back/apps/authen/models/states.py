from django.db import models

from apps.commons.models.base_table import BaseTable


class States(BaseTable):
    """Модель государств"""
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        unique=True,
        default='Новое государство',
        verbose_name='Наименование государства'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Государство'
        verbose_name_plural = 'Государства'
