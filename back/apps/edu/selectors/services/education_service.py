from django.apps import apps
from django.db.models import QuerySet
from django_filters import rest_framework as filters

education_service_model = apps.get_model('edu', 'EducationService')


def education_service_queryset() -> QuerySet:
    """Получение queryset с образоватльными услугами (курсами)"""
    return education_service_model.objects.all().order_by('-date_create')


class EducationServiceFilter(filters.FilterSet):
    """Поля для фильтрации образовательных услуг (курсов)"""
    program = filters.CharFilter(method='filter_program')
    location = filters.CharFilter(lookup_expr='icontains')
    date_start = filters.DateFilter()
    date_end = filters.DateFilter()

    def filter_program(self, queryset, name, value):
        return queryset.filter(program__name__icontains=value)
