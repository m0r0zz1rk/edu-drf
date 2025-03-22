from django.db import models

from apps.commons.models import BaseTable
from apps.edu.consts.student_group.type import STUDENT_GROUP_TYPES


class StudentAnswer(BaseTable):
    """Модель ответов обучающихся на вопросы опроса"""
    survey = models.ForeignKey(
        'surveys.Survey',
        on_delete=models.CASCADE,
        related_name='student_answers',
        null=False,
        verbose_name='Опрос'
    )
    group_code = models.CharField(
        max_length=100,
        default='Код группы',
        verbose_name='Код учебной группы'
    )
    group_type = models.CharField(
        choices=STUDENT_GROUP_TYPES,
        max_length=5,
        default='edu',
        verbose_name='Тип учебной группы'
    )
    question = models.TextField(
        max_length=500,
        blank=True,
        default='',
        verbose_name='Формулировка вопроса'
    )
    answer = models.TextField(
        max_length=500,
        blank=True,
        default='',
        verbose_name='Ответ обучающегося'
    )

    def __str__(self):
        return (f'Ответ пользователя на вопрос "{self.question}" опроса "{self.survey}"'
                f' (ID: {self.object_id})')

    class Meta:
        verbose_name = 'Ответ обучающегося'
        verbose_name_plural = 'Ответы обучающихся'
