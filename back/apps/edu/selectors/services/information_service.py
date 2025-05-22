from django.apps import apps
from django.db.models import QuerySet
from django_filters import rest_framework as filters

from apps.commons.orm.base_orm import BaseORM

# Модель мероприятий (ИКУ)
information_service_model = apps.get_model('edu', 'InformationService')

# Класс ORM для мероприятий ИКУ (ОУ)
information_service_orm = BaseORM(
    model=information_service_model,
    select_related=['department', 'type'],
    prefetch_related=['categories']
)


def information_service_queryset() -> QuerySet:
    """Получение queryset с информационно-консультационными услугами (мероприятиями)"""
    return information_service_orm.get_filter_records(order_by=['-date_create'])
    # return information_service_model.objects.all().order_by('-date_create')


class InformationServiceFilter(filters.FilterSet):
    """Поля для фильтрации образовательных услуг (курсов)"""
    dep = filters.CharFilter(method='filter_dep')
    department = filters.CharFilter(method='filter_department')
    type = filters.CharFilter(method='filter_type')
    name = filters.CharFilter(lookup_expr='icontains')
    location = filters.CharFilter(lookup_expr='icontains')
    date_start = filters.DateFilter()
    date_end = filters.DateFilter()

    def filter_dep(self, queryset, name, value):
        """Фильтрация по подразделению (для сотрудников центров)"""
        return queryset.filter(department__object_guid=value)

    def filter_department(self, queryset, name, value):
        return queryset.filter(department__display_name__icontains=value)

    def filter_type(self, queryset, name, value):
        """Фильтрация по наименованию типа мероприятия"""
        return queryset.filter(type__name__icontains=value)
