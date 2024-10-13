from rest_framework import serializers

from apps.guides.selectors.mo import mo_model


class MoBaseSerializer(serializers.ModelSerializer):
    """Базовая сериализация данных при работе с МО в модуле Справочники"""
    class Meta:
        model = mo_model
        fields = ['name', ]


class MoListUpdateSerializer(MoBaseSerializer):
    """Сериализация данных при получении списка муниципальных образований в модуле Справочники"""
    object_id = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label="UUID МО"
    )

    class Meta:
        model = mo_model
        fields = MoBaseSerializer.Meta.fields + ['object_id', ]
