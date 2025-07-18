from django.apps import apps
from django.db.models import QuerySet

from apps.commons.orm.base_orm import BaseORM

# Модель документов об оплате
pay_doc_model = apps.get_model('docs', 'PayDoc')

# Класс ORM для работы с документами об оплате
pay_doc_orm = BaseORM(
    model=pay_doc_model,
    select_related=['profile',]
)


def pay_doc_queryset() -> QuerySet:
    """Получение queryset со всеми документами об оплате"""
    return pay_doc_model.objects.select_related('profile').all().order_by(
        'profile__surname',
        'profile__name',
        'profile__patronymic'
    )
