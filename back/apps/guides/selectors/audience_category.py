from django.apps import apps
from django.db.models import QuerySet

audience_category_model = apps.get_model('guides', 'AudienceCategory')


def audience_category_queryset() -> QuerySet:
    """Получение queryset с категориями слушателей"""
    return audience_category_model.objects.all().order_by('name')