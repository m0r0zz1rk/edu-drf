import os

from django.db import models

from apps.commons.models import BaseTable
from apps.commons.utils.django.settings import SettingsUtils
from apps.docs.consts.student_doc_types import STUDENT_DOC_TYPES, DIPLOMA


def get_student_doc_upload_path(instance, filename) -> str:
    """
    Получение пути загрузки документа обучающегося
    :param instance: сущность файла (получаем из FileField)
    :param filename: имя файла (получаем из FileField)
    :return: Путь для загрузки
    """
    file_name, file_extension = os.path.splitext(filename)
    new_file_name = (f"{''.join(symb for symb in file_name if symb == ' ' or symb.isalnum())}"
                     f"{file_extension}")
    doc_path = SettingsUtils().get_parameter_from_settings('MEDIA_ROOT')
    doc_type_folder = instance.doc_type
    for dt in STUDENT_DOC_TYPES:
        if dt[0] == instance.doc_type:
            doc_type_folder = dt[1]
    spl = instance.profile.display_name.split(' ')
    user_folder = spl[0]
    if len(spl) > 1:
        try:
            user_folder += f' {spl[1][0]}'
        except Exception:
            pass
    if len(spl) > 2:
        try:
            user_folder += f' {spl[2][0]}'
        except Exception:
            pass
    for subfolder in ['Документы пользователей', doc_type_folder, user_folder]:
        doc_path = os.path.join(doc_path, subfolder)
        if not os.path.exists(doc_path):
            os.makedirs(doc_path)
    return os.path.join(doc_path, new_file_name)


class StudentDoc(BaseTable):
    """Модель документов обучающихся"""
    profile = models.ForeignKey(
        'authen.StudentProfile',
        on_delete=models.CASCADE,
        verbose_name='Студент'
    )
    doc_type = models.CharField(
        choices=STUDENT_DOC_TYPES,
        max_length=25,
        default=DIPLOMA,
        verbose_name='Тип документа'
    )
    file = models.FileField(
        upload_to=get_student_doc_upload_path,
        null=True,
        max_length=4000,
        verbose_name='Файл документа'
    )

    def __str__(self):
        for dt in STUDENT_DOC_TYPES:
            if dt[0] == self.doc_type:
                return f'{dt[1]} № {self.object_id} от {self.date_create.strftime("%d.%m.%Y")}'

    def delete(self, *args, **kwargs):
        """Удаление файла после удаления записи"""
        path = self.file.path
        # Удаляем сначала модель ( объект )
        super(StudentDoc, self).delete(*args, **kwargs)
        # Потом удаляем сам файл
        os.remove(path)

    class Meta:
        verbose_name = 'Документ обучающегося'
        verbose_name_plural = 'Документы обучающегося'
