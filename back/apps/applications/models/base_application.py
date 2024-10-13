from django.db import models

from apps.applications.consts.application_statuses import APPLICATION_STATUSES, DRAFT
from apps.commons.models import BaseTable


class BaseApplication(BaseTable):
    """Базовая модель заявок обучающихся"""
    profile = models.ForeignKey(
        'authen.StudentProfile',
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Профиль обучающегося'
    )
    group = models.ForeignKey(
        'edu.StudentGroup',
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Учебная группа'
    )
    status = models.CharField(
        max_length=25,
        choices=APPLICATION_STATUSES,
        default=DRAFT,
        verbose_name='Статус'
    )
    pay_doc = models.ForeignKey(
        'docs.PayDoc',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Документ об оплате'
    )
    check_survey = models.BooleanField(
        default=False,
        verbose_name='Опрос пройден'
    )
    work_less = models.BooleanField(
        default=False,
        verbose_name='Обучающийся безработный'
    )
    region = models.ForeignKey(
        'guides.Region',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Регион РФ'
    )
    mo = models.ForeignKey(
        'guides.Mo',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='МО (если регион - Иркутская область)'
    )
    oo = models.ForeignKey(
        'guides.Oo',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='ОО (из справочника)'
    )
    oo_new = models.CharField(
        max_length=1500,
        blank=True,
        default='',
        verbose_name='ОО (не из справочника)'
    )
    position_category = models.ForeignKey(
        'guides.PositionCategory',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Категория должностей'
    )
    position = models.ForeignKey(
        'guides.Position',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Должность'
    )
    physical = models.BooleanField(
        default=True,
        verbose_name='Физическое лицо'
    )

    def __str__(self):
        return f'Заявка пользователя {self.profile.display_name} для группы {self.group.code}'

    class Meta:
        abstract = True
