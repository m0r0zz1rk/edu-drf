from django.apps import apps
from django.db.models import QuerySet
from django_filters import rest_framework as filters

from apps.commons.services.ad.ad_centre_coko_user import AdCentreCokoUserUtils

coko_profile_model = apps.get_model('authen', 'CokoProfile')


def coko_profile_queryset() -> QuerySet:
    """Получение queryset с сотрудниками ЦОКО"""
    return coko_profile_model.objects.all().order_by('surname', 'name', 'patronymic')


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
