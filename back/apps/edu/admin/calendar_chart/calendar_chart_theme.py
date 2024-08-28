from django.contrib import admin

from apps.edu.selectors.calender_chart.calendar_chart_theme import calendar_chart_theme_model


@admin.register(calendar_chart_theme_model)
class CalendarChartThemeAdmin(admin.ModelAdmin):
    """Отображение тем разделов КУГ в административной панели"""
    list_display = ('chapter_name', 'position', 'name')
    search_fields = ('chapter__name', 'name')

    def chapter_name(self, obj):
        """Отображение наименования раздела КУГ"""
        if obj.chapter is not None:
            return obj.chapter.name
        return '-'

    chapter_name.short_description = 'Раздел'
