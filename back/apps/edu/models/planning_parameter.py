from django.db import models

from apps.commons.models import BaseTable


class PlanningParameter(BaseTable):
    """Модель параметров планирования мероприятий"""
    name = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        null=False,
        default='Новый параметр',
        verbose_name='Наименование параметра'
    )
    description = models.CharField(
        max_length=1000,
        blank=True,
        default='',
        verbose_name='Описание параметра'
    )
    value = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        default='1',
        verbose_name='Значение параметра'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Параметр планирования'
        verbose_name_plural = 'Параметры планирования'
