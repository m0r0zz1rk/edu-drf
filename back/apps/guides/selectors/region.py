from django.apps import apps
from django.db.models import QuerySet

region_model = apps.get_model('guides', 'Region')


def region_queryset() -> QuerySet:
    """Получение queryset со всеми регионами РФ"""
    return region_model.objects.all().order_by('name')


def irkutsk_state_object() -> region_model:
    """Получение объекта региона 'Иркутская область' """
    try:
        return region_model.objects.get(name='Иркутская область')
    except Exception:
        return None
