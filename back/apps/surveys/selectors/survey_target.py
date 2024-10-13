from django.apps import apps
from django.db.models import QuerySet

from django_filters import rest_framework as filters

from apps.surveys.consts.survey_target_types import SURVEY_TARGET_TYPES

survey_target_model = apps.get_model('surveys', 'SurveyTarget')


def survey_target_model_queryset() -> QuerySet:
    """Получение списка всех назначений опросов"""
    return survey_target_model.objects.all()


class SurveyTargetFilter(filters.FilterSet):
    """Поля для фильтрации таргетирований опросов"""
    survey_description = filters.CharFilter(
        method='filter_survey_description',
        label='Описание опроса'
    )
    type = filters.CharFilter(
        method='filter_target_type',
        label='Тип таргетирования'
    )

    def filter_survey_description(self, queryset, name, value):
        return queryset.filter(survey__description__icontains=value)

    def filter_target_type(self, queryset, name, value):
        for type in SURVEY_TARGET_TYPES:
            if type[1] == value:
                return queryset.filter(type=type[0])
