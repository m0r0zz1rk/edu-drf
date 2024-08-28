from django.contrib import admin

from apps.commons.utils.lesson_time import LessonTimeUtils

ltu = LessonTimeUtils()


class ScheduleAdmin(admin.ModelAdmin):
    """Отображение модели расписания занятий учебной группы в административной панели"""
    list_display = (
        'group_code',
        'date',
        'time_start_text',
        'time_end_text',
        'theme',
        'lesson_type',
        'lesson_hours'
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

    def time_start_end(self, obj):
        """Отображение времени окончания занятия в формате ЧЧ:ММ"""
        return ltu.convert_seconds_to_time(obj.time_end)

    def lesson_type(self, obj):
        """Отображение типа занятия"""
        if obj.lecture_hours != 0:
            return 'Лекция'
        elif obj.practice_hours != 0:
            return 'Практика'
        elif obj.trainee_hours != 0:
            return 'Стажировка'
        else:
            return 'Самостоятельная работа'

    def lesson_hours(self, obj):
        """Отоюражение количества часов занятия"""
        if obj.lecture_hours != 0:
            return obj.lecture_hours
        elif obj.practice_hours != 0:
            return obj.practice_hours
        elif obj.trainee_hours != 0:
            return obj.trainee_hours
        else:
            return obj.individual_hours

    group_code.short_description = 'Шифр учебной группы'
    time_start_text.short_description = 'Начало занятия'
    time_start_end.short_description = 'Окончание занятия'
    lesson_type.short_description = 'Тип занятия'
    lesson_hours.short_description = 'Часов'
