from django_filters import rest_framework as filters


class NameFieldFilter(filters.FilterSet):
    """Поля для фильтрации моделей, содержащих только поле name"""
    name = filters.CharFilter(
        lookup_expr='icontains'
    )
