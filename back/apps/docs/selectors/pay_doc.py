from django.apps import apps
from django.db.models import QuerySet

pay_doc_model = apps.get_model('docs', 'PayDoc')


def pay_doc_queryset() -> QuerySet:
    """Получение queryset со всеми документами об оплате"""
    return pay_doc_model.objects.all().order_by(
        'profile__surname',
        'profile__name',
        'profile__patronymic'
    )
