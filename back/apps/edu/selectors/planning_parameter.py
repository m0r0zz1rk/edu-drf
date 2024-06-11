from django.apps import apps
from django.db.models import QuerySet
from django_filters import rest_framework as filters

planning_parameter_model = apps.get_model('edu', 'PlanningParameter')


def planning_parameter_queryset() -> QuerySet:
    """Получение queryset с параметрами планирования"""
    return planning_parameter_model.objects.all()


class PlanningParameterFilter(filters.FilterSet):
    """Поля для фильтрации параметров планирования"""
    description = filters.CharFilter(lookup_expr='icontains')
    value = filters.CharFilter(lookup_expr='icontains')
