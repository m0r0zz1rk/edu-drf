from django.db import models

from apps.commons.models import BaseTable


class PositionCategory(BaseTable):
    """Модель категорий должностей"""
    name = models.CharField(
        max_length=200,
        unique=True,
        blank=False,
        null=False,
        default='Новая категория должностей',
        verbose_name='Название категории должностей'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория должностей'
        verbose_name_plural = 'Категории должностей'
