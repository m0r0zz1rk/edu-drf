from django.db import models

from apps.commons.models import BaseTable


class Mo(BaseTable):
    """Модель муниципальных образований"""
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
        default='Новое муниципальное образование',
        verbose_name='Название муниципального образования'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Муниципальное образование'
        verbose_name_plural = 'Муниципальные образования'
