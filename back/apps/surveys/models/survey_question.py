from django.db import models

from apps.commons.models import BaseTable
from apps.surveys.consts.survey_question_type import SURVEY_QUESTION_TYPES


class SurveyQuestion(BaseTable):
    """Модель вопросов в опросах"""
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='questions',
        on_delete=models.CASCADE,
        verbose_name='Опрос'
    )
    sequence_number = models.PositiveIntegerField(
        default=1,
        verbose_name='Порядковый номер в опросе'
    )
    question_type = models.CharField(
        choices=SURVEY_QUESTION_TYPES,
        max_length=17,
        default='short',
        verbose_name='Тип вопроса'
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Формулировка вопроса'
    )

    def __str__(self):
        return f'{self.sequence_number}-й вопрос в опросе "{self.survey.description}"'

    class Meta:
        verbose_name = 'Вопрос опроса'
        verbose_name_plural = 'Вопросы опросов'
