from django.db import models

from apps.commons.models import BaseTable
from apps.guides.models import Mo, OoType


class Oo(BaseTable):
    """Модель образовательных организаций"""
    mo = models.ForeignKey(
        Mo,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Муниципальное образование'
    )
    short_name = models.CharField(
        max_length=150,
        blank=True,
        null=False,
        default='',
        verbose_name='Краткое наименование'
    )
    full_name = models.CharField(
        max_length=1000,
        blank=True,
        null=False,
        default='',
        verbose_name='Полное наименование'
    )
    oo_type = models.ForeignKey(
        OoType,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Тип образовательной организации'
    )
    form = models.CharField(
        max_length=150,
        blank=True,
        null=False,
        default='',
        verbose_name='Форма образовательной организации'
    )

    def __str__(self):
        return f'{self.short_name} (ID: {self.object_id})'

    class Meta:
        verbose_name = 'Образовательная организация'
        verbose_name_plural = 'Образовательные организации'
