import uuid

from django.apps import apps
from django.db.models import QuerySet
from django_filters import rest_framework as filters

from apps.commons.orm.base_orm import BaseORM
from apps.guides.selectors.profiles.student import student_profile_model

# Модель занятий расписания
schedule_model = apps.get_model('edu', 'Schedule')

# Класс ORM для работы с моделью занятий расписания
schedule_model_orm = BaseORM(
    model=schedule_model,
    select_related=['group', ]
)


def schedule_queryset(student_group_id: uuid = None) -> QuerySet:
    """
    Получение расписания занятий для учебной группы
    :param student_group_id: object_id учебной группы
    :return: queryset модели schedule
    """
    if student_group_id is None:
        return schedule_model_orm.get_filter_records(order_by=['date', ])
    return schedule_model_orm.get_filter_records(
        filter_by={'group_id': student_group_id},
        order_by=['date', ]
    )


def user_teachers_queryset() -> QuerySet:
    """Получение queryset со всеми внешними пользователями с параметром teacher=True"""
    return (student_profile_model.objects.
            select_related('django_user').
            select_related('state').
            filter(teacher=True))


class TeachersFilter(filters.FilterSet):
    """Поля для фильтрации преподавателей в расписание занятий"""
    surname = filters.CharFilter(lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    patronymic = filters.CharFilter(lookup_expr='icontains')
    phone = filters.CharFilter(lookup_expr='icontains')
