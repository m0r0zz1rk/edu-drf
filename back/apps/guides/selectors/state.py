from django.apps import apps
from django.db.models import QuerySet

state_model = apps.get_model('guides', 'State')


def state_queryset() -> QuerySet:
    """Получение QuerySet с государствами"""
    return state_model.objects.all().order_by('name')

