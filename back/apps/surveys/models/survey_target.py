from django.db import models

from apps.commons.models import BaseTable
from apps.surveys.consts.survey_target_types import SURVEY_TARGET_TYPES


class SurveyTarget(BaseTable):
    """Модель назначений опросов на учебные группы"""
    survey = models.OneToOneField(
        'surveys.Survey',
        on_delete=models.CASCADE,
        related_name='targets',
        null=False,
        verbose_name='Опрос'
    )
    type = models.CharField(
        choices=SURVEY_TARGET_TYPES,
        max_length=8,
        default='all',
        verbose_name='Тип назначения'
    )
    group = models.ForeignKey(
        'edu.StudentGroup',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name='survey_target',
        verbose_name='Учебная группа'
    )

    def __str__(self):
        return f'Назначение опроса "{self.survey}"'

    class Meta:
        verbose_name = 'Назначение опроса'
        verbose_name_plural = 'Назначения опросов'
