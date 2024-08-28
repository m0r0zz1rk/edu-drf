from django.contrib import admin

from apps.edu.selectors.student_group import student_group_model


@admin.register(student_group_model)
class StudentGroupAdmin(admin.ModelAdmin):
    """Отображение учебных групп в административной панели"""
    list_display = ('code', 'status')
    search_fields = ('code', )
