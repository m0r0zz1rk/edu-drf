from rest_framework import serializers


class SurveyQuestionsSerializer(serializers.Serializer):
    """Сериализация данных вопрос для прохождения опроса в заявке обучающегося"""
    object_id = serializers.UUIDField(
        allow_null=False,
        label='object_id вопроса'
    )
    text = serializers.CharField(
        max_length=500,
        allow_null=False,
        allow_blank=False,
        label='Формулировка вопроса'
    )
    type = serializers.CharField(
        max_length=6,
        allow_blank=False,
        allow_null=False,
        label='Тип вопроса'
    )
    options = serializers.ListSerializer(
        child=serializers.CharField(
            max_length=255,
            allow_null=True,
            allow_blank=False,
            label='Формулировка варианта ответа'
        ),
        allow_empty=True,
        label='Список вариантов ответов (при наличии)'
    )
