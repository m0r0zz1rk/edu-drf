from rest_framework import serializers


class BaseApplicationBulkDeleteSerializer(serializers.Serializer):
    """Сериализация данных при удалении нескольких заявок из учебной группы"""
    apps = serializers.ListField(
        child=serializers.UUIDField(allow_null=False),
        allow_empty=False
    )