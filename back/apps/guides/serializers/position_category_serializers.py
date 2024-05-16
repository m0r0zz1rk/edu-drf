from django.apps import apps
from rest_framework import serializers

position_category_model = apps.get_model('guides', 'PositionCategory')


class PositionCategoryBaseSerializer(serializers.ModelSerializer):
    """Базовая сериалазация данных при работе с категорями должностей в модуле Справочники"""
    class Meta:
        model = position_category_model
        fields = ['name', ]


class PositionCategoryListUpdateSerializer(PositionCategoryBaseSerializer):
    """Сериализация данных при получении списка или обновлении категорий должностей в модуле Справочники"""
    object_id = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        label='UUID типа ОО'
    )

    class Meta:
        model = position_category_model
        fields = PositionCategoryBaseSerializer.Meta.fields + ['object_id']

