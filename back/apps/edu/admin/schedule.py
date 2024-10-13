from django.contrib import admin

from apps.commons.utils.lesson_time import LessonTimeUtils
from apps.edu.selectors.schedule import schedule_model

ltu = LessonTimeUtils()


@admin.register(schedule_model)
class ScheduleAdmin(admin.ModelAdmin):
    """Отображение модели расписания занятий учебной группы в административной панели"""
    list_display = (
        'group_code',
        'date',
        'time_start_text',
        'time_end_text',
        'theme',
        'type',
    )

    search_fields = (
        'group__code',
        'theme'
    )

    def group_code(self, obj):
        """Отображение шифра учебной группы"""
        return obj.group.code

    def time_start_text(self, obj):
        """Отображение времени начала занятия в формате ЧЧ:ММ"""
        return ltu.convert_seconds_to_time(obj.time_start)

    def time_end_text(self, obj):
        """Отображение времени окончания занятия в формате ЧЧ:ММ"""
        return ltu.convert_seconds_to_time(obj.time_end)

    group_code.short_description = 'Шифр учебной группы'
    time_start_text.short_description = 'Начало занятия'
    time_end_text.short_description = 'Окончание занятия'
