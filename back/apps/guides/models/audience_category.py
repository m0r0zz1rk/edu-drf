from django.db import models

from apps.commons.models import BaseTable


class AudienceCategory(BaseTable):
    """Модель категорий слушателей"""
    name = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        blank=False,
        default='Новая категория слушателей',
        verbose_name='Название категории слушателей'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория слушателей'
        verbose_name_plural = 'Категории слушателей'
