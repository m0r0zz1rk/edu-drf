from django_filters import rest_framework as filters


class CokoFilter(filters.FilterSet):
    """Поля для фильтрации сотрудников ЦОКО"""
    surname = filters.CharFilter(lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    patronymic = filters.CharFilter(lookup_expr='icontains')
    curator_groups = filters.BooleanFilter()
