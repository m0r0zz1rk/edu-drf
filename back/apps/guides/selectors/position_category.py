from django.apps import apps
from django.db.models import QuerySet

position_category_model = apps.get_model('guides', 'PositionCategory')


def position_category_queryset() -> QuerySet:
    """Получение queryset с категориями должностей"""
    return position_category_model.objects.all().order_by('name')
