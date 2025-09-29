from django.apps import apps
from django.db.models import QuerySet, Q

from django_filters import rest_framework as filters

from apps.commons.orm.base_orm import BaseORM
from apps.guides.selectors.profiles.coko import coko_profile_model

# Модель опросов
survey_model = apps.get_model('surveys', 'Survey')

# Класс ORM для работы с опросами
survey_orm = BaseORM(model=survey_model, select_related=['creator', ])


def survey_queryset() -> QuerySet:
    """Получение списка опросов"""
    return survey_orm.get_filter_records()


class SurveyFilter(filters.FilterSet):
    """Поля для фильтрации опросов"""
    description = filters.CharFilter(lookup_expr='icontains', label='Описание опроса')
    creator_fio = filters.CharFilter(method='filter_creator_fio', label='ФИО создателя')

    def filter_creator_fio(self, queryset, name, value):
        user_ids = [coko.django_user_id for coko in coko_profile_model.objects.filter(
            Q(surname__contains=value) |
            Q(name__contains=value) |
            Q(patronymic__contains=value)
        )]
        return queryset.filter(creator_id__in=user_ids)
