from rest_framework import serializers


class RequestApplicationCreateSerializer(serializers.Serializer):
    """Сериализация данных при запросе на создании заявки"""
    group_id = serializers.UUIDField(
        allow_null=False,
        label='object_id учебной группы'
    )
