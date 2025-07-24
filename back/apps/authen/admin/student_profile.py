from django.contrib import admin

from apps.authen.models.student_profile import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """Класс для отображения профилей пользователей в административной панели"""

    list_display = (
        'state_name',
        'surname',
        'name',
        'patronymic',
        'birthday',
        'sex_alias',
        'phone',
        'snils'
    )
    search_fields = (
        'surname',
        'name',
        'patronymic',
        'phone',
        'snils'
    )

    def state_name(self, obj):
        """Отображение наименования государства"""
        if obj.state is not None:
            return obj.state.name
        return '-'

    def sex_alias(self, obj):
        """Отображение пола пользователя в текстовом формате"""
        if obj.sex:
            return 'М'
        return 'Ж'

    state_name.short_description = 'Государство'
    sex_alias.short_description = 'Пол'
