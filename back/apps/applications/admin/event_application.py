from django.contrib import admin

from apps.applications.selectors.event_application import (
    event_application_model)


@admin.register(event_application_model)
class EventApplicationAdmin(admin.ModelAdmin):
    """
    Класс для отображения заявок пользователей на
    участие в мероприятиях в административной панели
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
    student_display_name.description = 'ФИО студента'
