from django.contrib import admin

from apps.applications.selectors.course_application import (
    course_application_model)


@admin.register(course_application_model)
class CourseApplicationAdmin(admin.ModelAdmin):
    """
    Класс для отображения заявок на участие в
    курсах в административной панели
    """
    list_display = (
        'date_create',
        'group_code',
        'student_display_name',
        'status'
    )
    search_fields = (
        'group__code',
        'profile__surname',
        'profile__name',
        'profile__patronymic'
    )

    def group_code(self, obj):
        return obj.group.code

    def student_display_name(self, obj):
        return obj.profile.display_name

    group_code.short_description = 'Шифр группы'
    student_display_name.short_description = 'ФИО студента'
