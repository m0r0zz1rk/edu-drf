from django.contrib import admin

from apps.edu.selectors.calender_chart.calendar_chart_chapter import calendar_chart_chapter_model


@admin.register(calendar_chart_chapter_model)
class CalendarChartChapterAdmin(admin.ModelAdmin):
    """Отображение разделов КУГ в административной панели"""
    list_display = ('program_name', 'position', 'name')
    search_fields = ('program__name', 'name')

    def program_name(self, obj):
        """Отображение наименования ДПП"""
        if obj.program is not None:
            return obj.program.name
        return '-'

    program_name.short_description = 'ДПП'
