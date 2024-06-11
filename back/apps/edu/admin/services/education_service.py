from django.apps import apps
from django.contrib import admin

education_service_model = apps.get_model('edu', 'EducationService')


@admin.register(education_service_model)
class EducationServiceAdmin(admin.ModelAdmin):
    """Отображение образовательных услуг (курсов) в административной панели"""
    list_display = ('program', 'location', 'date_start', 'date_end')
    search_fields = ('program__name', 'location')

