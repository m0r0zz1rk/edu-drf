from django.apps import apps
from django.db.models import QuerySet

from apps.commons.orm.base_orm import BaseORM

# Модель типов образовательных организаций
oo_type_model = apps.get_model('guides', 'OoType')

# Класс ORM для типов образовательных организаций
oo_type_orm = BaseORM(model=oo_type_model)


def oo_type_queryset() -> QuerySet:
    """Получение queryset с типами ОО"""
    return oo_type_orm.get_filter_records(order_by=['name'])
