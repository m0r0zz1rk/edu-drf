from django.contrib import admin

from apps.docs.selectors.student_doc import student_doc_model


@admin.register(student_doc_model)
class StudentDocAdmin(admin.ModelAdmin):
    """Класс для отображения документов обучающихся в административной панели"""
    list_display = (
        'student_display_name',
        'doc_type',
        'file'
    )

    search_fields = (
        'profile__surname',
        'profile__name',
        'profile__patronymic'
        'doc_type',
    )

    def student_display_name(self, obj):
        """Получение ФИО пользователя"""
        return obj.profile.display_name

    student_display_name.short_description = 'Обучающийся'
