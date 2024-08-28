from django.contrib import admin

from apps.edu.selectors.services.education_service import education_service_model


@admin.register(education_service_model)
class EducationServiceAdmin(admin.ModelAdmin):
    """Отображение образовательных услуг (курсов) в административной панели"""
    list_display = ('program', 'location', 'date_start', 'date_end')
    search_fields = ('program__name', 'location')

