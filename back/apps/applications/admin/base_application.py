from django.contrib import admin


class BaseApplicationAdmin(admin.ModelAdmin):
    """
    Класс для отображения заявок пользователей в административной панели
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
