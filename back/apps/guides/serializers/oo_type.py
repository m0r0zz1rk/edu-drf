from rest_framework import serializers
from apps.guides.selectors.oo_type import oo_type_model


class OoTypeBaseSerializer(serializers.ModelSerializer):
    """Базовая сериалазация данных при работе с типами ОО в модуле Справочники"""
    class Meta:
        model = oo_type_model
        fields = ['name', ]


class OoTypeListUpdateSerializer(OoTypeBaseSerializer):
    """Сериализация данных при получении списка или обновлении типа ОО в модуле Справочники"""
    object_id = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        label='UUID типа ОО'
    )

    class Meta:
        model = oo_type_model
        fields = OoTypeBaseSerializer.Meta.fields + ['object_id']
