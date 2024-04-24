from django.db import models

from apps.commons.models import BaseTable


class State(BaseTable):
    """Модель государств"""
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        default='Новое государство',
        verbose_name='Название государства'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Государство'
        verbose_name_plural = 'Государства'
