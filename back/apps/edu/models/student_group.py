from django.db import models

from apps.commons.models import BaseTable
from apps.edu.consts.student_group.student_group_forms import STUDENT_GROUP_FORMS, WITHOUT
from apps.edu.consts.student_group.student_group_statuses import STUDENT_GROUP_STATUSES, REGISTRATION


class StudentGroup(BaseTable):
    """Модель учебных групп"""
    code = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        unique=True,
        default='НовыйШифр',
        verbose_name='Шифр'
    )
    ou = models.ForeignKey(
        'edu.EducationService',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        verbose_name='ОУ (курс)'
    )
    iku = models.ForeignKey(
        'edu.InformationService',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        verbose_name='ИКУ (мероприятие)'
    )
    curator = models.ForeignKey(
        'authen.CokoProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        verbose_name='Куратор'
    )
    plan_seats_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        default=None,
        verbose_name='Плановое количество мест (для ИКУ)'
    )
    status = models.CharField(
        max_length=40,
        choices=STUDENT_GROUP_STATUSES,
        default=REGISTRATION,
        verbose_name='Статус'
    )
    form = models.CharField(
        max_length=30,
        choices=STUDENT_GROUP_FORMS,
        default=WITHOUT,
        verbose_name='Форма обучения'
    )
    event_url = models.URLField(
        max_length=3000,
        blank=True,
        default='https://coko38.ru/',
        verbose_name='Ссылка на мероприятие'
    )
    survey_show = models.BooleanField(
        default=False,
        blank=True,
        verbose_name='Отображение опроса'
    )
    date_enroll = models.DateField(
        null=True,
        default=None,
        blank=True,
        verbose_name='Дата приказа о зачислении'
    )
    date_exp = models.DateField(
        null=True,
        default=None,
        blank=True,
        verbose_name='Дата приказа об отчислении'
    )
    enroll_number = models.CharField(
        max_length=50,
        default='',
        blank=True,
        verbose_name='Номер приказа о зачислении'
    )
    exp_number = models.CharField(
        max_length=50,
        default='',
        blank=True,
        verbose_name='Номер приказа об отчислении'
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'
