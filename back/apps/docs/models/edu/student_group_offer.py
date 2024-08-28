import os

from django.db import models

from apps.commons.models import BaseTable
from apps.docs.services.edu.student_group_offer import StudentGroupOfferService


class StudentGroupOffer(BaseTable):
    """Модель договоров оферты учебных групп"""
    student_group = models.ForeignKey(
        'edu.StudentGroup',
        on_delete=models.CASCADE,
        verbose_name='Учебная группа'
    )
    file = models.FileField(
        upload_to=StudentGroupOfferService().get_upload_path,
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
