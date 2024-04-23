from django.db import models

from apps.commons.models import BaseTable


class EventType(BaseTable):
    """Модель типов мероприятий"""
    name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        default='Новый тип мероприятий'
    )