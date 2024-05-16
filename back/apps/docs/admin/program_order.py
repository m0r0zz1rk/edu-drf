from django.apps import apps
from django.contrib import admin

program_order_model = apps.get_model('docs', 'ProgramOrder')


@admin.register(program_order_model)
class ProgramOrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'date')
    search_fields = ('number', 'date')
