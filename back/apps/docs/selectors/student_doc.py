from django.apps import apps
from django.db.models import QuerySet
from django_filters import rest_framework as filters

from apps.docs.consts.student_doc_types import STUDENT_DOC_TYPES

student_doc_model = apps.get_model('docs', 'StudentDoc')


def student_doc_queryset() -> QuerySet:
    """QuerySet со всеми документами пользователей"""
    return student_doc_model.objects.select_related('profile').all().order_by('-date_create')


class StudentDocFilter(filters.FilterSet):
    """Поля для фильтрации документов обучающихся"""
    date_create = filters.DateFilter(
        label='Дата добавления документа'
    )
    doc_type = filters.CharFilter(
        method='filter_doc_type',
        label='Тип документа'
    )

    def filter_doc_type(self, queryset, name, value):
        """Фильтрация по типу документа"""
        doc_type = value
        for type in STUDENT_DOC_TYPES:
            if type[1] == value:
                doc_type = type[0]
        return queryset.filter(doc_type=doc_type)
