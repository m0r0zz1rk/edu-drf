from django.db import models

from apps.commons.models import BaseTable


class CourseCertificate(BaseTable):
    """
    Модель сертификатов обучающихся на курсах (ОУ)
    """
    application = models.ForeignKey(
        'applications.CourseApplication',
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Заявка на курс (ОУ)'
    )
    registration_number = models.CharField(
        max_length=50,
        null=False,
        blank=True,
        default='',
        verbose_name='Порядковый регистрационный номер'
    )
    blank_serial = models.CharField(
        max_length=50,
        null=False,
        blank=True,
        default='',
        verbose_name='Серия бланка удостоверения'
    )
    blank_number = models.CharField(
        max_length=50,
        null=False,
        blank=True,
        default='',
        verbose_name='Номер бланка удостоверения'
    )

    def __str__(self):
        fio = '(не назначена)'
        group = self.object_id
        if self.application:
            fio = (f'{self.application.profile.surname} '
                   f'{self.application.profile.name} '
                   f'{self.application.profile.patronymic}')
            group = self.application.group.code
        if group == self.object_id:
            return f'Сертификат (ID: {self.object_id})'
        return f'Сертификат обучающегося "{fio}" в группе "{group}"'

    class Meta:
        verbose_name = 'Сертификат обучающегося'
        verbose_name_plural = 'Сертификаты обучающегося'
