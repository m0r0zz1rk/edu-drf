from django.apps import apps
from django.contrib import admin

program_model = apps.get_model('edu', 'Program')


@admin.register(program_model)
class ProgramAdmin(admin.ModelAdmin):
    """Отображение ДПП в административной панели"""
    list_display = ('name', )
    search_fields = ('name', )
