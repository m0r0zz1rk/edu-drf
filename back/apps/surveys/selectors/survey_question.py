from django.apps import apps
from django.db.models import QuerySet

from django_filters import rest_framework as filters

from apps.surveys.consts.survey_question_type import SURVEY_QUESTION_TYPES

survey_question_model = apps.get_model('surveys', 'SurveyQuestion')


def survey_question_queryset() -> QuerySet:
    """
    Получение всех вопросов опросов
    """
    return survey_question_model.objects.all().order_by('sequence_number')


class SurveyQuestionFilter(filters.FilterSet):
    """Поля для фильтрации вопросов опроса"""
    survey_id = filters.CharFilter(
        method='filter_survey_id',
        label='object_id опроса'
    )
    sequence_number = filters.NumberFilter(
        label='Порядковый номер вопроса'
    )
    text = filters.CharFilter(lookup_expr='icontains', label='Формулировка вопроса')
    question_type = filters.CharFilter(
        method='filter_question_type',
        label='Тип вопроса'
    )

    def filter_survey_id(self, queryset, name, value):
        return queryset.filter(survey_id=value)

    def filter_question_type(self, queryset, name, value):
        tp = None
        for q_t in SURVEY_QUESTION_TYPES:
            if q_t[1] == value:
                tp = q_t[0]
                break
        if tp is None:
            return queryset
        return queryset.filter(question_type=tp)
