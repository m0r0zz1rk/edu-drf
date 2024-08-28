from django.contrib import admin

from apps.edu.selectors.program import program_model


@admin.register(program_model)
class ProgramAdmin(admin.ModelAdmin):
    """Отображение ДПП в административной панели"""
    list_display = ('name', )
    search_fields = ('name', )
