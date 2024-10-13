from django.contrib.auth.models import User
from django.db import models

from apps.commons.models import BaseTable


class Survey(BaseTable):
    """Модель опросов"""
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Создатель опроса'
    )
    description = models.CharField(
        max_length=1500,
        blank=False,
        default='Новый опрос',
        verbose_name='Описание опроса'
    )

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
