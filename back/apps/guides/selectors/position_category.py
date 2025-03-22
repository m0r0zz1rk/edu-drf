from django.apps import apps
from django.db.models import QuerySet

from apps.commons.orm.base_orm import BaseORM

# Модель категорий должностей
position_category_model = apps.get_model('guides', 'PositionCategory')

# Класс ORM для категорий должностей
position_category_orm = BaseORM(model=position_category_model)


def position_category_queryset() -> QuerySet:
    """Получение queryset с категориями должностей"""
    return position_category_orm.get_filter_records(order_by=['name'])
