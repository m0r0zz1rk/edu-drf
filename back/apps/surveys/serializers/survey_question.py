from rest_framework import serializers

from apps.surveys.consts.survey_question_type import SURVEY_QUESTION_TYPES
from apps.surveys.selectors.survey_question import survey_question_model


class SurveyQuestionListSerializer(serializers.ModelSerializer):
    """Сериализация данных для получения списка вопросов опроса"""

    question_type = serializers.SerializerMethodField(
        label='Тип вопроса'
    )

    def get_question_type(self, obj):
        for q_t in SURVEY_QUESTION_TYPES:
            if q_t[0] == obj.question_type:
                return q_t[1]
        return obj.question_type

    class Meta:
        model = survey_question_model
        exclude = ('date_create', 'survey')


class SurveyQuestionBaseSerializer(serializers.ModelSerializer):
    """Базовая сериализация информации о вопросе опроса"""

    class Meta:
        model = survey_question_model
        fields = (
            'sequence_number',
            'text'
        )


class SurveyQuestionCreateSerializer(SurveyQuestionBaseSerializer):
    """Сериализация данных для добавления вопроса опроса"""
    survey_id = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label='object_id опроса'
    )
    question_type = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label='Тип вопроса'
    )

    class Meta(SurveyQuestionBaseSerializer.Meta):
        fields = SurveyQuestionBaseSerializer.Meta.fields + ('survey_id', 'question_type')


class SurveyQuestionUpdateSerializer(serializers.ModelSerializer):
    """Сериализация данных при обновлении вопроса опроса"""
    class Meta:
        model = survey_question_model
        exclude = ('date_create', )
