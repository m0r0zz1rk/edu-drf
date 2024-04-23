from django.db import models

from apps.commons.models import BaseTable


class OoType(BaseTable):
    """Модель типов образовательных организаций"""
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        default='Новый тип образовательной организации',
        verbose_name='Наименование типа образовательной организации'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип образовательной организации'
        verbose_name_plural = 'Типы образовательных организаций'
