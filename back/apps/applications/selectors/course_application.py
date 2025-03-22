from django.apps import apps
from django.db.models import QuerySet
from apps.commons.orm.base_orm import BaseORM

# Модель типов мероприятий
course_application_model = apps.get_model('applications', 'CourseApplication')

# Список связанных полей
select_related = [
    'profile',
    'group',
    'pay_doc',
    'region',
    'mo',
    'oo',
    'position_category',
    'position',
    'education_doc',
    'surname_doc',
    'certificate_doc'
]

# Класс ORM для типов мероприятий
course_application_orm = BaseORM(
    model=course_application_model,
    select_related=select_related
)


def course_application_queryset() -> QuerySet:
    """Получение queryset со всем заявками на участие в курсах"""
    return course_application_orm.get_filter_records(
        order_by=['profile__surname', 'profile__name', 'profile__patronymic']
    )
