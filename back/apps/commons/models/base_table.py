import uuid

from django.db import models


class BaseTable(models.Model):
    """Базовая модель БД"""
    object_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID объекта'
    )
    old_id = models.PositiveIntegerField(
        default=0,
        verbose_name='ID объекта из олдовой БД edu'
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )

    objects = models.Manager()

    class Meta:
        db_table = "[schema].[table]"
        abstract = True
