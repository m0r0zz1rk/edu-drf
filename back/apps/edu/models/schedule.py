import datetime

from django.db import models

from apps.commons.models import BaseTable
from apps.commons.utils.lesson_time import LessonTimeUtils
from apps.edu.consts.lesson_types import LESSON_TYPES


class Schedule(BaseTable):
    """Модель расписания занятий учебной группы"""
    group = models.ForeignKey(
        'edu.StudentGroup',
        on_delete=models.CASCADE,
        verbose_name='Учебная группа'
    )
    date = models.DateField(
        default=datetime.date.today,
        verbose_name='Дата занятия'
    )
    time_start = models.PositiveIntegerField(
        default=0,
        verbose_name='Время начала занятия (в секундах)'
    )
    time_end = models.PositiveIntegerField(
        default=0,
        verbose_name='Время окончания занятия (в секундах)'
    )
    kug_theme = models.ForeignKey(
        'edu.CalendarChartTheme',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        verbose_name='Тема из КУГ (для групп по курсам)'
    )
    theme = models.CharField(
        max_length=500,
        null=False,
        blank=False,
        default='Тема',
        verbose_name='Тема занятия'
    )
    type = models.CharField(
        max_length=25,
        choices=LESSON_TYPES,
        default='lecture',
        null=False,
        blank=False,
        verbose_name='Тип занятия'
    )
    teacher = models.UUIDField(
        null=True,
        default=None,
        verbose_name='object_id профиля преподавателя'
    )
    distance = models.BooleanField(
        default=False,
        verbose_name='Дистанционное занятие'
    )
    control = models.CharField(
        max_length=150,
        null=True,
        default=None,
        verbose_name='Контрольное занятие'
    )

    def __str__(self):
        return (f'Занятие группы {self.group.code} {self.data.strftime("%d.%m.%Y")} в '
                f'{LessonTimeUtils.convert_seconds_to_time(self.time_start)}')

    class Meta:
        verbose_name = 'Занятие учебной группы'
        verbose_name_plural = 'Занятия учебных групп'
