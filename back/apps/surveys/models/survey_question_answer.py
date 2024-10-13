from django.db import models

from apps.commons.models import BaseTable


class SurveyQuestionAnswer(BaseTable):
    """Модель заготовленных ответов на вопросы опроса"""
    survey_question = models.ForeignKey(
        'surveys.SurveyQuestion',
        related_name='answers',
        on_delete=models.CASCADE,
        null=True,
        default=None,
        verbose_name='Вопрос опроса'
    )
    text = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Текст ответа'
    )

    def __str__(self):
        return f'Ответ для "{self.survey_question}"'

    class Meta:
        verbose_name = 'Ответ вопроса'
        verbose_name_plural = 'Ответы вопросов'
