import datetime

from django.db import models

from apps.applications.consts.education import EDUCATION_LEVELS, EDUCATION_CATEGORIES, HIGHER
from apps.applications.models.base_application import BaseApplication


class CourseApplication(BaseApplication):
    """Модель заявок обучающихся на прохождение курса"""
    education_level = models.CharField(
        max_length=75,
        choices=EDUCATION_LEVELS,
        default=HIGHER,
        verbose_name='Уровень образования'
    )
    education_category = models.CharField(
        max_length=75,
        choices=EDUCATION_CATEGORIES,
        default=HIGHER,
        verbose_name='Категория получаемого образования (при уровне образования - студент)'
    )
    education_doc = models.ForeignKey(
        'docs.StudentDoc',
        related_name='education_doc',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Документ об образовании'
    )
    education_check = models.BooleanField(
        default=False,
        verbose_name='Документ об образовании проверен'
    )
    diploma_surname = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name='Фамилия в дипломе'
    )
    surname_doc = models.ForeignKey(
        'docs.StudentDoc',
        related_name='surname_doc',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Документ о смене фамилии'
    )
    education_serial = models.CharField(
        max_length=30,
        blank=True,
        default='',
        verbose_name='Серия документа об образовании'
    )
    education_number = models.CharField(
        max_length=30,
        blank=True,
        default='',
        verbose_name='Номер документа об образовании'
    )
    education_date = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата выдачи документа об образовании'
    )
    certificate_doc = models.ForeignKey(
        'docs.StudentDoc',
        related_name='certificate_doc',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Скан удостоверения'
    )
    certificate_mail = models.BooleanField(
        default=False,
        verbose_name='Получение сертификата по почте'
    )
    mail_address = models.TextField(
        max_length=5000,
        blank=True,
        default='',
        verbose_name='Физический адрес доставки сертификата по почте'
    )

    class Meta:
        verbose_name = 'Заявка на участие в курсе'
        verbose_name_plural = 'Заявки на участие в курсах'
