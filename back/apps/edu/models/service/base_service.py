import datetime

from django.db import models

from apps.commons.models import BaseTable


class BaseService(BaseTable):
    """Базовая модель услуг"""
    location = models.CharField(
        max_length=500,
        null=False,
        blank=True,
        default='',
        verbose_name='Место проведения'
    )
    date_start = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата начала оказания услуги'
    )
    date_end = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата окончания оказания услуги'
    )

    class Meta:
        abstract = True
