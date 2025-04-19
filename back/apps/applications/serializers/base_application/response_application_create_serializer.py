from rest_framework import serializers


class ResponseApplicationCreateSerializer(serializers.Serializer):
    """Сериализация данных ответа на запрос на создание заявки"""
    app_id = serializers.UUIDField(
        allow_null=False,
        label='object_id созданной заявки'
    )


class ApplicationCreateSerializer(serializers.Serializer):
    """
    Сериализация данных при запросе на создание заявки
    """
    group_id = serializers.UUIDField(
        allow_null=False,
        label='object_id учебной группы'
    )
