from rest_framework import serializers

from apps.surveys.selectors.survey_question import survey_question_model


class SurveyQuestionListSerializer(serializers.ModelSerializer):
    """Сериализация данных для получения списка вопросов опроса"""
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
