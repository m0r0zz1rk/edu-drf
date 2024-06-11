from django.apps import apps
from rest_framework import serializers

mo_model = apps.get_model('guides', 'Mo')


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


