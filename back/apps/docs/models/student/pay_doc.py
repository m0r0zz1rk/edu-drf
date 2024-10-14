import os

from django.db import models

from apps.commons.models import BaseTable
from apps.commons.utils.django.settings import SettingsUtils


def get_pay_doc_upload_path(instance, filename) -> str:
    """
    Получение пути загрузки документа об оплате
    :param instance: объект документа об оплате
    :param filename: имя файла (получаем из FileField)
    :return: Путь для загрузки
    """
    file_name, file_extension = os.path.splitext(filename)
    new_file_name = (f"{''.join(symb for symb in file_name if symb == ' ' or symb.isalnum())}"
                     f"{file_extension}")
    doc_path = SettingsUtils().get_parameter_from_settings('MEDIA_ROOT')
    for subfolder in [
        'Документы об оплате',
        f'{instance.profile.display_name}_{instance.profile.birthday.strftime("%d-%m-%Y")}'
    ]:
        doc_path = os.path.join(doc_path, subfolder)
        if not os.path.exists(doc_path):
            os.makedirs(doc_path)
    return os.path.join(doc_path, new_file_name)


class PayDoc(BaseTable):
    """Модель документов об оплате обучающихся за услугу"""
    profile = models.ForeignKey(
        'authen.StudentProfile',
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Профиль обучающегося'
    )
    pay_file = models.FileField(
        upload_to=get_pay_doc_upload_path,
        null=True,
        max_length=4000,
        verbose_name='Файл документа'
    )

    def __str__(self):
        return (f'Документ об оплате пользователя {self.profile.display_name} в группе '
                f'{self.group.code} (ID: {self.object_id}')

    class Meta:
        verbose_name = 'Документ об оплате'
        verbose_name_plural = 'Документы об оплате'
