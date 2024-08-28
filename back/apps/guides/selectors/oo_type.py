from django.apps import apps
from django.db.models import QuerySet

oo_type_model = apps.get_model('guides', 'OoType')


def oo_type_queryset() -> QuerySet:
    """Получение queryset с типами ОО"""
    return oo_type_model.objects.all().order_by('name')

