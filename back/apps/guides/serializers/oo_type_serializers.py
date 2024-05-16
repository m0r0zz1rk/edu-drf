from django.apps import apps
from rest_framework import serializers

oo_type_model = apps.get_model('guides', 'OoType')


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
