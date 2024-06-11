from django.apps import apps
from django_filters import rest_framework as filters

oo_model = apps.get_model('guides', 'Oo')


class OoFilter(filters.FilterSet):
    """Поля для фильтрации ОО"""
    mo = filters.CharFilter(method='filter_mo')
    short_name = filters.CharFilter(lookup_expr='icontains')
    full_name = filters.CharFilter(lookup_expr='icontains')
    oo_type = filters.CharFilter(method='filter_oo_type')
    form = filters.CharFilter(lookup_expr='icontains')

    def filter_mo(self, queryset, name, value):
        return queryset.filter(mo__name__icontains=value)

    def filter_oo_type(self, queryset, name, value):
        return queryset.filter(oo_type__name__icontains=value)

    class Meta:
        model = oo_model
        exclude = ['object_id', 'date_create']
