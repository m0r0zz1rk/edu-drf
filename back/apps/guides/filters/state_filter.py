from django_filters import rest_framework as filters


class StateFilter(filters.FilterSet):
    """Поля для фильтрации государств"""
    name = filters.CharFilter(
        lookup_expr='icontains'
    )
