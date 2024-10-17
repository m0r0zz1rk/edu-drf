from django.apps import apps
from django.db.models import QuerySet

from django_filters import rest_framework as filters

survey_question_answer_model = apps.get_model('surveys', 'SurveyQuestionAnswer')


def survey_question_answer_queryset() -> QuerySet:
    """
    Получение списка возможных ответов на вопросы опросов
    """
    return (survey_question_answer_model.objects.
            select_related('survey_question').
            all())


class SurveyQuestionAnswerFilter(filters.FilterSet):
    """Поля для фильтрации возможных ответов вопроса опроса"""
    survey_question_id = filters.CharFilter(
        method='filter_survey_question_id',
        label='object_id опроса'
    )
    text = filters.CharFilter(lookup_expr='icontains', label='Формулировка вопроса')

    def filter_survey_question_id(self, queryset, name, value):
        return queryset.filter(survey_question_id=value)
