from django.db import models

from apps.edu.models.calendar_chart.calendar_chart_element import CalendarChartElement


class CalendarChartChapter(CalendarChartElement):
    """Модель разделов КУГ ДПП"""

    program = models.ForeignKey(
        'edu.Program',
        on_delete=models.CASCADE,
        null=False,
        verbose_name='ДПП'
    )

    def __str__(self):
        try:
            return f'Раздел № {self.position} "{self.name}" (ДПП: {self.program.name}) '
        except Exception:
            return 'Раздел КУГа ДПП'

    class Meta:
        verbose_name = 'Раздел КУГа'
        verbose_name_plural = 'Разделы КУГа'
