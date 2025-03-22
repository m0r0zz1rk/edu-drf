from django.apps import apps
from django.db.models import QuerySet
from django_filters import rest_framework as filters

from apps.commons.orm.base_orm import BaseORM

# Модель дополнительных профессиональных программ
program_model = apps.get_model('edu', 'Program')

# Класс ORM для дополнительных профессиональных программ
program_orm = BaseORM(
    model=program_model,
    select_related=['department', 'kug_edit', 'program_order'],
    prefetch_related=['categories']
)


def program_queryset() -> QuerySet:
    """Получение queryset с ДПП"""
    return program_orm.get_filter_records(order_by=['-date_create', ])


def approved_program_queryset() -> QuerySet:
    """Получение queryset ДПП с установленными приказами"""
    return program_orm.get_filter_records(exclude={'program_order_id': None}, order_by=['-date_create'], )


class ProgramFilter(filters.FilterSet):
    """Поля для фильтрации ДПП"""
    name = filters.CharFilter(lookup_expr='icontains')
    duration = filters.NumberFilter(lookup_expr='exact')
    department = filters.CharFilter(method='filter_department')
    order_number = filters.CharFilter(method='filter_order_number')
    order_date = filters.DateFilter(method='filter_order_date')

    def filter_department(self, queryset, name, value):
        return queryset.select_related('department').filter(department__display_name__icontains=value)

    def filter_order_number(self, queryset, name, value):
        return queryset.filter(program_order__number__icontains=value)

    def filter_order_date(self, queryset, name, value):
        return queryset.filter(program_order__date__icontains=value)
