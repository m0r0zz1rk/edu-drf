from datetime import datetime

from django.apps import apps
from django.db.models import QuerySet, Q
from django_filters import rest_framework as filters

from apps.commons.orm.base_orm import BaseORM

from apps.edu.consts.student_group.statuses import STUDENT_GROUP_STATUSES, COMPLETE

# Модель учебных групп
student_group_model = apps.get_model('edu', 'StudentGroup')

# Класс ORM для учебных групп
student_group_orm = BaseORM(
    model=student_group_model,
    select_related=['ou', 'iku', 'curator']
)


def student_group_queryset() -> QuerySet:
    """Получение queryset с учебными группами"""
    return student_group_orm.get_filter_records(order_by=['-date_create',])


class StudentGroupFilter(filters.FilterSet):
    """Поля для фильтрации ДПП"""
    dep = filters.CharFilter(method="filter_dep")
    code = filters.CharFilter(lookup_expr='icontains')
    service_name = filters.CharFilter(method="filter_service_name")
    date_start = filters.CharFilter(method="filter_date_start")
    date_end = filters.CharFilter(method='filter_date_end')
    month = filters.CharFilter(method="filter_month")
    year = filters.CharFilter(method="filter_year")
    curator = filters.CharFilter(method='filter_curator')
    apps_count = filters.CharFilter(method='filter_apps_count')
    status = filters.CharFilter(method='filter_status')

    def filter_dep(self, queryset, name, value):
        """Фильтрация по подразделению (для сотрудников центров)"""
        return queryset.filter(
            Q(ou__program__department__object_guid=value) |
            Q(iku__department__object_guid=value)
        )

    def filter_service_name(self, queryset, name, value):
        """Фильтрация по наименованию услуги"""
        return queryset.filter(
            Q(ou__program__name__contains=value) |
            Q(iku__name__contains=value)
        )

    def filter_date_start(self, queryset, name, value):
        """Фильтрация по дате начала оказания услуги"""
        return queryset.filter(
            Q(ou__date_start=datetime.strptime(value, '%d.%m.%Y').date()) |
            Q(iku__date_start=datetime.strptime(value, '%d.%m.%Y').date())
        )

    def filter_date_end(self, queryset, name, value):
        """Фильтрация по дате окончания оказания услуги"""
        return queryset.filter(
            Q(ou__date_end=datetime.strptime(value, '%d.%m.%Y').date()) |
            Q(iku__date_end=datetime.strptime(value, '%d.%m.%Y').date())
        )

    def filter_month(self, queryset, name, value):
        """Фильтрация по месяцу (для отчета ФИС ФРДО)"""
        int_value = int(value)
        if int_value == 0:
            return queryset
        return queryset.filter(
            Q(ou__date_start__month=int_value) |
            Q(ou__date_end__month=int_value)
        )

    def filter_year(self, queryset, name, value):
        """Фильтрация по году (для отчета ФИС ФРДО)"""
        int_value = int(value)
        if int_value == 0:
            return queryset
        return queryset.filter(
            Q(ou__date_start__year=int_value) |
            Q(ou__date_end__year=int_value)
        )

    def filter_curator(self, queryset, name, value):
        """Фильтрация по ФИО куратора"""
        return queryset.filter(
            Q(curator__surname__contains=value) |
            Q(curator__name__contains=value) |
            Q(curator__patronymic__contains=value)
        )

    def filter_apps_count(self, queryset, name, value):
        """Фильтрация по количеству заявок"""
        return queryset

    def filter_status(self, queryset, name, value):
        """Фильтрация по статусу учебной группы"""
        if value == 'not_complete':
            return queryset.exclude(status=COMPLETE)
        for k, v in STUDENT_GROUP_STATUSES:
            if v == value:
                return queryset.filter(status=k)
