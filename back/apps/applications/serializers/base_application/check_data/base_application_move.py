from rest_framework import serializers


class AppMoveSerializer(serializers.Serializer):
    """
    Сериализация данных для переноса одной заявки из учебной группы в другую
    """
    application_id = serializers.UUIDField(
        allow_null=False,
        label='object_id заявки для переноса'
    )
    group_id = serializers.UUIDField(
        allow_null=False,
        label='object_id учебной группы назначения'
    )


class AppMoveAllSerializer(serializers.Serializer):
    """
    Сериализация данных для переноса всех заявок из одной учебной группы в другую
    """
    source_group_id = serializers.UUIDField(
        allow_null=False,
        label='object_id учебной группы источника'
    )
    destination_group_id = serializers.UUIDField(
        allow_null=False,
        label='object_id учебной группы назначения'
    )
