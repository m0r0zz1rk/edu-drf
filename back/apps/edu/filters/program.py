from django_filters import rest_framework as filters


class ProgramFilter(filters.FilterSet):
    """Поля для фильтрации ДПП"""
    name = filters.CharFilter(lookup_expr='icontains')
    duration = filters.NumberFilter(lookup_expr='exact')
    department = filters.CharFilter(method='filter_department')
    order_number = filters.CharFilter(method='filter_order_number')
    order_date = filters.DateFilter(method='filter_order_date')

    def filter_department(self, queryset, name, value):
        return queryset.filter(department__display_name__icontains=value)

    def filter_order_number(self, queryset, name, value):
        return queryset.filter(program_order__number__icontains=value)

    def filter_order_date(self, queryset, name, value):
        return queryset.filter(program_order__date__icontains=value)
