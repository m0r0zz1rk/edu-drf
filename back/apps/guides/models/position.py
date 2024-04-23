from django.db import models

from apps.commons.models import BaseTable


class Position(BaseTable):
    """Модель должностей"""
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        default='Новая должность',
        verbose_name='Наименование должности'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
