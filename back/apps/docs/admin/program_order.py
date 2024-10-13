from django.contrib import admin

from apps.docs.selectors.program_order import program_order_model


@admin.register(program_order_model)
class ProgramOrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'date')
    search_fields = ('number', 'date')
