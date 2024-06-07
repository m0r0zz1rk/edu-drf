from django.core.validators import MinValueValidator
from django.db import models

from apps.commons.models import BaseTable


class CalendarChartElement(BaseTable):
    """Модель базовых элементов каледнарного учебного графика (КУГ)"""
    position = models.PositiveIntegerField(
        validators=[MinValueValidator(1),],
        verbose_name='Позиция относительно остальных элементов данного уровня'
    )
    name = models.CharField(
        max_length=500,
        default='Наименование',
        null=False,
        blank=False,
        verbose_name='Наименование модуля (раздела)'
    )
    total_hours = models.PositiveIntegerField(
        verbose_name='Общее количество часов'
    )
    lecture_hours = models.PositiveIntegerField(
        verbose_name='Количество лекционных часов'
    )
    practice_hours = models.PositiveIntegerField(
        verbose_name='Количество часов практики'
    )
    trainee_hours = models.PositiveIntegerField(
        verbose_name='Количество часов стажировок'
    )
    individual_hours = models.PositiveIntegerField(
        verbose_name='Количество часов самостоятельной работы'
    )
    control_form = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Форма контроля'
    )

    def __str__(self):
        return f'{self.name} ({self.object_id})'

    class Meta:
        abstract = True
        verbose_name = 'Базовый элемент КУГ'
        verbose_name_plural = 'Базовые элементы КУГ'
