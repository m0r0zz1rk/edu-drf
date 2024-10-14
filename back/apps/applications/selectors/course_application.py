from django.apps import apps
from django.db.models import QuerySet, Q

from django_filters import rest_framework as filters

from apps.applications.consts.application_statuses import APPLICATION_STATUSES

course_application_model = apps.get_model('applications', 'CourseApplication')


def course_application_queryset() -> QuerySet:
    """Получение queryset со всем заявками на участие в курсах"""
    return course_application_model.objects.all().order_by(
        'profile__surname',
        'profile__name',
        'profile__patronymic'
    )


class CourseApplicationFilter(filters.FilterSet):
    """Поля для фильтрации заявок в таблице учебной группы"""
    student = filters.CharFilter(
        method='filter_student',
        label='Информация по студенту'
    )
    date_create = filters.DateFilter(
        input_formats=['%d.%m.%Y'],
        label='Дата подачи заявки'
    )
    status = filters.CharFilter(
        method="filter_status",
        label='Статус заявки'
    )

    def filter_student(self, queryset, name, value):
        """Фильтрация по ФИО, email или номеру телефона обучающегося"""
        return queryset.filter(
            Q(profile__surname__contains=value) |
            Q(profile__name__contains=value) |
            Q(profile__patronymic__contains=value) |
            Q(profile__django_user__email__contains=value) |
            Q(profile__phone__contains=value)
        )

    def filter_status(self, queryset, name, value):
        """Фильтрация по статусу заявки"""
        for st in APPLICATION_STATUSES:
            if st[1] == value:
                return queryset.filter(status=st[0])

