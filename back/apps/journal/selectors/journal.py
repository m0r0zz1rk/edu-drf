import datetime

from django.apps import apps
from django.db.models import Q, QuerySet
from django_filters import rest_framework as filters

from apps.commons.orm.base_orm import BaseORM
from apps.journal.consts.journal_modules import JOURNAL_MODULES
from apps.journal.consts.journal_rec_statuses import JOURNAL_REC_STATUSES

# Модель журнала событий
journal_model = apps.get_model('journal', 'Journal')

# Класс ORM для журнаоа событий
journal_orm = BaseORM(model=journal_model)

def journal_queryset() -> QuerySet:
    """Получение queryset с записями журнала"""
    return journal_orm.get_filter_records(order_by=['-date_create', ])


class JournalFilter(filters.FilterSet):
    """Поля для фильтрации записей журнала"""
    date_create = filters.CharFilter(method='filter_date_create')
    source = filters.CharFilter(
        lookup_expr='icontains'
    )
    module = filters.CharFilter(method='filter_module')
    status = filters.CharFilter(method='filter_status')
    description = filters.CharFilter(
        lookup_expr='icontains'
    )

    def filter_date_create(self, queryset, name, value):
        get_day = datetime.datetime.strptime(value, '%d.%m.%Y')
        tomorrow = get_day + datetime.timedelta(days=1)
        queryset = queryset.filter(
            Q(date_create__gte=get_day) &
            Q(date_create__lt=tomorrow)
        )
        return queryset

    def filter_module(self, queryset, name, value):
        filter_value = ''
        for source, display in JOURNAL_MODULES:
            if display == value:
                filter_value = source
                break
        queryset = queryset.filter(module=filter_value)
        return queryset

    def filter_status(self, queryset, name, value):
        filter_value = ''
        for source, display in JOURNAL_REC_STATUSES:
            if display == value:
                filter_value = source
                break
        queryset = queryset.filter(status=filter_value)
        return queryset

    class Meta:
        model = journal_model
        exclude = ('object_id',)
