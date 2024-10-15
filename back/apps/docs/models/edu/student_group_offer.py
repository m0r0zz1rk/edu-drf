import os

from django.db import models

from apps.commons.models import BaseTable
from apps.commons.utils.django.settings import SettingsUtils


def get_upload_path(instance, filename) -> str:
    """
    Получение пути загрузки файлов
    :param instance: сущность файла (получаем из FileField)
    :param filename: имя файла (получаем из FileField)
    :return: Путь для загрузки
    """
    _, file_extension = os.path.splitext(filename)
    new_file_name = f"{''.join(symb for symb in instance.group.code if symb == ' ' or symb.isalnum())}{file_extension}"
    order_path = SettingsUtils().get_parameter_from_settings('MEDIA_ROOT')
    for subfolder in ['Договора', 'Оферта', instance.group.code]:
        order_path = os.path.join(order_path, subfolder)
        if not os.path.exists(order_path):
            os.makedirs(order_path)
    return os.path.join(order_path, new_file_name)


class StudentGroupOffer(BaseTable):
    """Модель договоров оферты учебных групп"""
    group = models.ForeignKey(
        'edu.StudentGroup',
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Учебная группа'
    )
    file = models.FileField(
        upload_to=get_upload_path,
        null=True,
        max_length=1000,
        verbose_name='Договор оферты'
    )

    def __str__(self):
        return f'Договор оферты группы {self.student_group.code}'

    def delete(self, *args, **kwargs):
        """Удаление файла после удаления записи"""
        path = self.file.path
        # Удаляем сначала модель ( объект )
        super(StudentGroupOffer, self).delete(*args, **kwargs)
        # Потом удаляем сам файл
        os.remove(path)

    class Meta:
        verbose_name = 'Договор оферты учебной группы'
        verbose_name_plural = 'Договора оферты учебных групп'
