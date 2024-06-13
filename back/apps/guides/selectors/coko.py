from django_filters import rest_framework as filters

from apps.commons.services.ad.ad_centre_coko_user import AdCentreCokoUserUtils


class CokoFilter(filters.FilterSet):
    """Поля для фильтрации сотрудников ЦОКО"""
    surname = filters.CharFilter(lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    patronymic = filters.CharFilter(lookup_expr='icontains')
    curator_groups = filters.BooleanFilter()
    department = filters.CharFilter(method='filter_department')

    def filter_department(self, queryset, name, value):
        ids = AdCentreCokoUserUtils().get_centre_user_ids_by_display_name(value)
        return queryset.filter(django_user_id__in=ids)
