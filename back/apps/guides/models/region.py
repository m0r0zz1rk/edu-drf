from django.db import models

from apps.commons.models import BaseTable


class Region(BaseTable):
    """Модель регионов РФ"""
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        default='Новый регион',
        unique=True,
        verbose_name='Название региона'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион РФ'
        verbose_name_plural = 'Регионы РФ'
