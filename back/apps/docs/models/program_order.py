import datetime
import os

from django.db import models

from apps.commons.models import BaseTable
from apps.docs.utils.program_order import ProgramOrderUtils


class ProgramOrder(BaseTable):
    """Модель приказов об утверждении ДПП"""
    number = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        default='___',
        verbose_name='Номер приказа'
    )
    date = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата приказа'
    )
    file = models.FileField(
        upload_to=ProgramOrderUtils().get_upload_path,
        null=True,
        max_length=1000,
        verbose_name='Файл приказа'
    )

    def __str__(self):
        return f'{self.number} от {self.date.strftime("%d.%m.%Y")}'

    def delete(self, *args, **kwargs):
        """Удаление файла после удаления записи"""
        path = self.file.path
        # Удаляем сначала модель ( объект )
        super(ProgramOrder, self).delete(*args, **kwargs)
        # Потом удаляем сам файл
        os.remove(path)

    class Meta:
        verbose_name = 'Приказ об утверждении ДПП'
        verbose_name_plural = 'Приказы об утверждении ДПП'
