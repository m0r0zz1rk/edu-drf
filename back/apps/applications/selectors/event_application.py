from django.apps import apps
from django.db.models import QuerySet

from apps.commons.orm.base_orm import BaseORM

# Модель типов мероприятий
event_application_model = apps.get_model('applications', 'EventApplication')

# Список связанных полей
select_related = [
    'profile',
    'group',
    'pay_doc',
    'region',
    'mo',
    'oo',
    'position_category',
    'position'
]

# Класс ORM для типов мероприятий
event_application_orm = BaseORM(
    model=event_application_model,
    select_related=select_related
)


def event_application_queryset() -> QuerySet:
    """Получение queryset со всем заявками на участие в мероприятиях"""
    return event_application_orm.get_filter_records(
        order_by=['profile__surname', 'profile__name', 'profile__patronymic']
    )
