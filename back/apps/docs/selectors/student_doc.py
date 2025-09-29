from django.apps import apps
from django.db.models import QuerySet
from django_filters import rest_framework as filters

from apps.commons.orm.base_orm import BaseORM
from apps.docs.consts.student_doc_types import STUDENT_DOC_TYPES

# Модель документов обучающихся
student_doc_model = apps.get_model('docs', 'StudentDoc')

# Класс ORM для работы с документами обучающихся
student_doc_orm = BaseORM(model=student_doc_model, select_related=['profile',])


def student_doc_queryset() -> QuerySet:
    """QuerySet со всеми документами пользователей"""
    return student_doc_orm.get_filter_records(order_by=['-date_create',])


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
