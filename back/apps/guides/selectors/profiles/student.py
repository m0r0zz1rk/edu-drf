import datetime

from django.db.models import Q, QuerySet
from django_filters import rest_framework as filters

from apps.authen.selectors.student_profile import student_profile_orm, student_profile_model


def student_profile_queryset() -> QuerySet:
    """Получение queryset c профилями обучающихся"""
    return student_profile_orm.get_filter_records(order_by=['surname', 'name', 'patronymic'])


class UserFilter(filters.FilterSet):
    """Поля для фильтрации пользователей"""
    date_create = filters.CharFilter(method='filter_date_create')
    state = filters.AllValuesFilter(field_name='state__name')
    surname = filters.CharFilter(lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    patronymic = filters.CharFilter(lookup_expr='icontains')
    birthday = filters.DateFilter(lookup_expr='exact')
    snils = filters.CharFilter(lookup_expr='icontains')
    sex = filters.BooleanFilter()
    phone = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(method='filter_email')
    teacher = filters.BooleanFilter()
    health = filters.BooleanFilter()
    curator_groups = filters.BooleanFilter()

    def filter_date_create(self, queryset, name, value):
        get_day = datetime.datetime.strptime(value, '%d.%m.%Y')
        tomorrow = get_day + datetime.timedelta(days=1)
        queryset = queryset.filter(
            Q(date_create__gte=get_day) &
            Q(date_create__lt=tomorrow)
        )
        return queryset

    def filter_email(self, queryset, name, value):
        return queryset.filter(
            django_user__email__icontains=value
        )

    class Meta:
        model = student_profile_model
        exclude = ['django_user', 'object_id']
