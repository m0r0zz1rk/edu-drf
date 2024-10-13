import datetime
import os

from django.db import models

from apps.commons.models import BaseTable
from apps.commons.utils.django.settings import SettingsUtils


def get_program_order_upload_path(instance, filename) -> str:
    """
    Получение пути загрузки приказов об утверждении ДПП
    :param instance: сущность файла (получаем из FileField)
    :param filename: имя файла (получаем из FileField)
    :return: Путь для загрузки
    """
    _, file_extension = os.path.splitext(filename)
    new_file_name = f"{''.join(symb for symb in instance.number if symb == ' ' or symb.isalnum())}{file_extension}"
    order_path = SettingsUtils().get_parameter_from_settings('MEDIA_ROOT')
    for subfolder in ['Приказы', 'ДПП']:
        order_path = os.path.join(order_path, subfolder)
        if not os.path.exists(order_path):
            os.makedirs(order_path)
    return os.path.join(order_path, new_file_name)

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
        upload_to=get_program_order_upload_path,
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
