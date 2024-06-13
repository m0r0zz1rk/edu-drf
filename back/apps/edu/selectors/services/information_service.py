from django.apps import apps
from django.db.models import QuerySet
from django_filters import rest_framework as filters

information_service_model = apps.get_model('edu', 'InformationService')


def information_service_queryset() -> QuerySet:
    """Получение queryset с информационно-консультационными услугами (мероприятиями)"""
    return information_service_model.objects.all().order_by('-date_create')


class InformationServiceFilter(filters.FilterSet):
    """Поля для фильтрации образовательных услуг (курсов)"""
    department = filters.CharFilter(method='filter_department')
    type = filters.CharFilter(method='filter_type')
    name = filters.CharFilter(lookup_expr='icontains')
    location = filters.CharFilter(lookup_expr='icontains')
    date_start = filters.DateFilter()
    date_end = filters.DateFilter()

    def filter_department(self, queryset, name, value):
        return queryset.filter(department__display_name__icontains=value)

    def filter_type(self, queryset, name, value):
        """Фильтрация по наименованию типа мероприятия"""
        return queryset.filter(type__name__icontains=value)
