from django.db import models

from apps.commons.models import BaseTable, AdCentre
from apps.docs.models import ProgramOrder
from apps.guides.models import AudienceCategory


class Program(BaseTable):
    """Модель дополнительных професиональных программ"""
    department = models.ForeignKey(
        AdCentre,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Подразделение'
    )
    name = models.CharField(
        max_length=500,
        null=False,
        blank=False,
        default='Новая программа',
        verbose_name='Наименование программы'
    )
    type = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        default='Повышение квалификации',
        verbose_name='Тип программы'
    )
    duration = models.PositiveIntegerField(
        default=0,
        verbose_name='Объем программы (часов)'
    )
    categories = models.ManyToManyField(
        AudienceCategory,
       verbose_name='Категории слушателей'
    )
    annotation = models.TextField(
        max_length=1500,
        verbose_name='Аннотация'
    )
    program_order = models.ForeignKey(
        ProgramOrder,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Приказ об утверждении ДПП'
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name='Стоимость'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дополнительная профессиональная программа'
        verbose_name_plural = 'Дополнительные профессиональные программы'
