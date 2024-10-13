from django.apps import apps
from django.db.models import QuerySet

event_type_model = apps.get_model('guides', 'EventType')


def event_type_queryset() -> QuerySet:
    """Получение queryset с типами мероприятий"""
    return event_type_model.objects.all().order_by('name')
