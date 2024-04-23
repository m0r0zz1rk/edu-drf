from rest_framework import serializers


class StateSerializer(serializers.Serializer):
    """Сериализация информации о государстве"""
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=200,)


class StatesSerializer(serializers.Serializer):
    """Сериализация списка государств"""
    states = StateSerializer(many=True)
