from django.apps import apps
from django.contrib import admin

information_service_model = apps.get_model('edu', 'InformationService')


@admin.register(information_service_model)
class InformationServiceAdmin(admin.ModelAdmin):
    """Отображение информационно-консультационных услуг (мероприятий) в административной панели"""
    list_display = (
        'department',
        'type',
        'name',
        'location',
        'date_start',
        'date_end'
    )
    search_fields = (
        'department__display_name',
        'type__name',
        'name',
        'location'
    )

