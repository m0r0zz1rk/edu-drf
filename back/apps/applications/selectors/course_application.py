from django.apps import apps
from django.db.models import QuerySet
from django_filters import rest_framework as filters

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


class CourseApplicationFilter(filters.FilterSet):
    """Поля для фильтрации заявок на курсы (ЛК пользователя)"""
    service_type = filters.CharFilter(method='filter_service_type')
    group_code = filters.CharFilter(method='filter_group_code')
    service_title = filters.CharFilter(method='filter_service_title')

    def filter_service_type(self, queryset, name, value):
        return queryset.filter(group__ou__program__type__icontains=value)

    def filter_group_code(self, queryset, name, value):
        return queryset.filter(group__code__icontains=value)

    def filter_service_title(self, queryset, name, value):
        return queryset.filter(group__ou__program__name__icontains=value)
