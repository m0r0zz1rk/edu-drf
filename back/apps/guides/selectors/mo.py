from django.apps import apps
from django.db.models import QuerySet

mo_model = apps.get_model('guides', 'Mo')


def mo_queryset() -> QuerySet:
    """Получение queryset с муниципальными образованиями"""
    return mo_model.objects.all().order_by('name')