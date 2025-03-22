from django.apps import apps
from django.db.models import QuerySet

from apps.commons.orm.base_orm import BaseORM

# Модель типов мероприятий
event_type_model = apps.get_model('guides', 'EventType')

# Класс ORM для типов мероприятий
event_type_orm = BaseORM(model=event_type_model)


def event_type_queryset() -> QuerySet:
    """Получение queryset с типами мероприятий"""
    return event_type_orm.get_filter_records(order_by=['name'])





