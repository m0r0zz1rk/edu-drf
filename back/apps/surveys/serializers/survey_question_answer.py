from rest_framework import serializers

from apps.surveys.selectors.survey_question_answer import survey_question_answer_model


class SurveyQuestionAnswerBaseSerializer(serializers.ModelSerializer):
    """Базовая сериализация данных для возможных ответов на вопрос опроса"""
    class Meta:
        model = survey_question_answer_model
        fields = (
            'object_id',
            'text'
        )


class SurveyQuestionAnswerCreateSerializer(serializers.ModelSerializer):
    """Сериализация данных при добавлении возможного ответа вопроса"""

    survey_question_id = serializers.UUIDField(
        allow_null=False,
        label='object_id вопроса опроса'
    )

    class Meta:
        model = survey_question_answer_model
        fields = (
            'survey_question_id',
            'text'
        )


class SurveyQuestionAnswerUpdateSerializer(SurveyQuestionAnswerCreateSerializer):
    """Сериализация данных при обновлении возможного ответа вопроса"""
    class Meta(SurveyQuestionAnswerCreateSerializer.Meta):
        fields = SurveyQuestionAnswerCreateSerializer.Meta.fields + ('object_id', )
