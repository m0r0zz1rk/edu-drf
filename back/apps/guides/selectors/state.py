from django.apps import apps
from django.db.models import QuerySet

from apps.commons.orm.base_orm import BaseORM

# Модель государств
state_model = apps.get_model('guides', 'State')

# Класс ORM для государств
state_orm = BaseORM(model=state_model)


def state_queryset() -> QuerySet:
    """Получение QuerySet с государствами"""
    return state_orm.get_filter_records(order_by=['name', ])
