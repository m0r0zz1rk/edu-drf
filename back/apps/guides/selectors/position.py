from django.apps import apps
from django.db.models import QuerySet

position_model = apps.get_model('guides', 'Position')


def position_queryset() -> QuerySet:
    """Получение queryset с должностями"""
    return position_model.objects.all().order_by('name')
