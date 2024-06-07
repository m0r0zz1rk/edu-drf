from django.db import models

from apps.edu.models.calendar_chart.calendar_chart_chapter import CalendarChartChapter
from apps.edu.models.calendar_chart.calendar_chart_element import CalendarChartElement


class CalendarChartTheme(CalendarChartElement):
    """Модель тем разделов КУГ ДПП"""
    chapter = models.ForeignKey(
        CalendarChartChapter,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Раздел КУГ ДПП'
    )

    def __str__(self):
        try:
            return (f'Тема № {self.position} "{self.name}" для раздела "{self.chapter.name}" КУГа '
                    f'ДПП "{self.chapter.program.name}"')
        except:
            return 'Тема раздела КУГа ДПП'

    class Meta:
        verbose_name = 'Тема раздела КУГа ДПП'
        verbose_name_plural = 'Темы разделов КУГов ДПП'
