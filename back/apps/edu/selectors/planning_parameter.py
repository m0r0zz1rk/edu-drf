from django.apps import apps
from django.db.models import QuerySet
from django_filters import rest_framework as filters

from apps.commons.orm.base_orm import BaseORM

# Модель параметров планирования услуг
planning_parameter_model = apps.get_model('edu', 'PlanningParameter')

# Класс ORM для работы с моделью параметров планирования услуг
planning_parameter_orm = BaseORM(
    model=planning_parameter_model
)


def planning_parameter_queryset() -> QuerySet:
    """Получение queryset с параметрами планирования"""
    return planning_parameter_orm.get_filter_records()


class PlanningParameterFilter(filters.FilterSet):
    """Поля для фильтрации параметров планирования"""
    description = filters.CharFilter(lookup_expr='icontains')
    value = filters.CharFilter(lookup_expr='icontains')
