from rest_framework import serializers

from apps.guides.selectors.position import position_model


class PositionBaseSerializer(serializers.ModelSerializer):
    """Базовая сериалазация данных при работе с должностями в модуле Справочники"""
    class Meta:
        model = position_model
        fields = ['name', ]


class PositionListUpdateSerializer(PositionBaseSerializer):
    """Сериализация данных при получении списка или обновлении должностями в модуле Справочники"""
    object_id = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        label='UUID типа ОО'
    )

    class Meta:
        model = position_model
        fields = PositionBaseSerializer.Meta.fields + ['object_id']

