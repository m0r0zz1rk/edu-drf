from django.apps import apps
from django.db.models import QuerySet

from apps.commons.orm.base_orm import BaseORM

# Модель муниципальных образований
mo_model = apps.get_model('guides', 'Mo')

# Класс ORM для муниципальных образований
mo_orm = BaseORM(model=mo_model)


def mo_queryset() -> QuerySet:
    """Получение queryset с муниципальными образованиями"""
    return mo_orm.get_filter_records(order_by=['name'])
