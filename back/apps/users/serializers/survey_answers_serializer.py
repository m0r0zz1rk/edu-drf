from rest_framework import serializers


class AnswerSerializer(serializers.Serializer):
    """Сериализация данных одного ответа на вопрос опроса"""
    question_id = serializers.UUIDField(
        allow_null=False,
        label='object_id вопроса опроса'
    )
    value = serializers.CharField(
        max_length=500,
        allow_null=False,
        allow_blank=False,
        label='Ответ обучающегося'
    )


class SurveyAnswersSerializer(serializers.Serializer):
    """Сериализация данных с ответами на вопросы опроса"""
    data = AnswerSerializer(
        many=True,
        label='Данные с ответами на вопрос'
    )
