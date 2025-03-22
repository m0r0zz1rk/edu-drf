from django.apps import apps
from django.db.models import QuerySet

from apps.commons.orm.base_orm import BaseORM

# Модель регионов
region_model = apps.get_model('guides', 'Region')

# Класс ORM для регионов
region_orm = BaseORM(model=region_model)


def region_queryset() -> QuerySet:
    """Получение queryset со всеми регионами РФ"""
    return region_orm.get_filter_records(order_by=['name'])
    # return region_model.objects.all().order_by('name')


def irkutsk_state_object() -> region_model:
    """Получение объекта региона 'Иркутская область' """
    try:
        return region_orm.get_one_record_or_none({'name': 'Иркутская область'})
    except Exception:
        pass
