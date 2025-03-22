from django.apps import apps
from django.db.models import QuerySet

from apps.commons.orm.base_orm import BaseORM

# Модель категорий слушателей
audience_category_model = apps.get_model('guides', 'AudienceCategory')

# Класс ORM для типов мероприятий
audience_category_orm = BaseORM(model=audience_category_model)


def audience_category_queryset() -> QuerySet:
    """Получение queryset с категориями слушателей"""
    return audience_category_orm.get_filter_records(order_by=['name', ])
