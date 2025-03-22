from django.db.models import Q
from django_filters import rest_framework as filters

from apps.applications.consts.application_statuses import APPLICATION_STATUSES


class ApplicationFilter(filters.FilterSet):
    """Поля для фильтрации заявок обучающихся"""
    group = filters.CharFilter(
        method='filter_group',
        label='Учебная группа (по коду)'
    )
    group_id = filters.CharFilter(
        method='filter_group_id',
        label='Учебная группа (по UUID)'
    )
    profile = filters.CharFilter(
        method='filter_profile',
        label='Профиль студента'
    )
    student = filters.CharFilter(
        method='filter_student',
        label='Информация по студенту'
    )
    date_create = filters.DateFilter(
        input_formats=['%d.%m.%Y'],
        label='Дата подачи заявки'
    )
    status = filters.CharFilter(
        method="filter_status",
        label='Статус заявки'
    )

    def filter_group(self, queryset, name, value):
        """Фильтрация по коду учебной группы"""
        return queryset.filter(group__code__contains=value)

    def filter_group_id(self, queryset, name, value):
        """Фильтрация по ID учебной группы"""
        return queryset.filter(group_id=value)

    def filter_profile(self, queryset, name, value):
        """Фильтрация по UUID профиля"""
        return queryset.filter(profile_id=value)

    def filter_student(self, queryset, name, value):
        """Фильтрация по ФИО, email или номеру телефона обучающегося"""
        return queryset.filter(
            Q(profile__surname__contains=value) |
            Q(profile__name__contains=value) |
            Q(profile__patronymic__contains=value) |
            Q(profile__django_user__email__contains=value) |
            Q(profile__phone__contains=value)
        )

    def filter_status(self, queryset, name, value):
        """Фильтрация по статусу заявки"""
        for st in APPLICATION_STATUSES:
            if st[1] == value:
                return queryset.filter(status=st[0])