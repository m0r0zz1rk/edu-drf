from django.apps import apps
from django.contrib import admin

planning_parameter_model = apps.get_model('edu', 'PlanningParameter')


@admin.register(planning_parameter_model)
class PlanningParameterAdmin(admin.ModelAdmin):
    """Отображение параметров планирования в административной панели"""
    list_display = ('name', 'description', 'value')
    search_fields = ('name', 'description')
