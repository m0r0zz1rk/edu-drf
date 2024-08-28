from django.contrib import admin

from apps.edu.selectors.planning_parameter import planning_parameter_model


@admin.register(planning_parameter_model)
class PlanningParameterAdmin(admin.ModelAdmin):
    """Отображение параметров планирования в административной панели"""
    list_display = ('name', 'description', 'value')
    search_fields = ('name', 'description')
