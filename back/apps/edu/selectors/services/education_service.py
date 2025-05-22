from django.apps import apps
from django.db.models import QuerySet
from django_filters import rest_framework as filters

from apps.commons.orm.base_orm import BaseORM

# Модель курсов (ОУ)
education_service_model = apps.get_model('edu', 'EducationService')

# Класс ORM для курсов (ОУ)
education_service_orm = BaseORM(
    model=education_service_model,
    select_related=['program',]
)


def education_service_queryset() -> QuerySet:
    """Получение queryset с образовательными услугами (курсами)"""
    return education_service_orm.get_filter_records(order_by=['-date_create',])


class EducationServiceFilter(filters.FilterSet):
    """Поля для фильтрации образовательных услуг (курсов)"""
    dep = filters.CharFilter(method='filter_dep')
    program = filters.CharFilter(method='filter_program')
    location = filters.CharFilter(lookup_expr='icontains')
    date_start = filters.DateFilter()
    date_end = filters.DateFilter()

    def filter_dep(self, queryset, name, value):
        """Фильтрация по подразделению (для сотрудников центров)"""
        return queryset.filter(program__department__object_guid=value)

    def filter_program(self, queryset, name, value):
        return queryset.filter(program__name__icontains=value)
