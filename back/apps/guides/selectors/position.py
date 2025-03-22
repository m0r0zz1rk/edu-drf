from django.apps import apps
from django.db.models import QuerySet

from apps.commons.orm.base_orm import BaseORM

# Модель должностей
position_model = apps.get_model('guides', 'Position')

# Класс ORM для должностей
position_orm = BaseORM(model=position_model)


def position_queryset() -> QuerySet:
    """Получение queryset с должностями"""
    return position_orm.get_filter_records(order_by=['name'])
