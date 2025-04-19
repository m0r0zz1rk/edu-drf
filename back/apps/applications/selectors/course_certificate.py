from django.apps import apps
from django.db.models import QuerySet, Q
from django_filters import rest_framework as filters

from apps.commons.orm.base_orm import BaseORM

# Модель сертификатов обучающихся
course_certificate_model = apps.get_model('applications', 'CourseCertificate')

# Класс ORM для работы с сертификатами обучающихся
course_certificate_orm = BaseORM(
    model=course_certificate_model,
    select_related=['application',]
)


def course_certificate_queryset() -> QuerySet:
    """Получение queryset со всем удостоверениями к заявкам на курсы"""
    return course_certificate_orm.get_filter_records(
        order_by=[
            'application__profile__surname',
            'application__profile__name',
            'application__profile__patronymic'
        ]
    )


class CourseCertificateFilter(filters.FilterSet):
    """Поля для фильтрации удостоверений к заявкам на куурсы"""
    group = filters.CharFilter(
        method='filter_group',
        label='Учебная группа (по коду)'
    )
    student = filters.CharFilter(
        method='filter_student',
        label='Информация по студенту'
    )
    registration_number = filters.CharFilter(
        lookup_expr='icontains',
        label='Порядковый регистрационный номер'
    )
    blank_serial = filters.CharFilter(
        lookup_expr='icontains',
        label='Серия бланка удостоверения'
    )
    blank_number = filters.CharFilter(
        lookup_expr='icontains',
        label='Номер бланка удостоверения'
    )

    def filter_group(self, queryset, name, value):
        """Фильтрация по коду учебной группы"""
        return queryset.filter(application__group__code__contains=value)

    def filter_student(self, queryset, name, value):
        """Фильтрация по ФИО, email или номеру телефона обучающегося"""
        return queryset.filter(
            Q(application__profile__surname__contains=value) |
            Q(application__profile__name__contains=value) |
            Q(application__profile__patronymic__contains=value) |
            Q(application__profile__django_user__email__contains=value) |
            Q(application__profile__phone__contains=value)
        )
