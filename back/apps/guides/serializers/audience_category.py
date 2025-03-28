from rest_framework import serializers

from apps.guides.selectors.audience_category import audience_category_model


class AudienceCategoryBaseSerializer(serializers.ModelSerializer):
    """Базовая сериалазация данных при работе с категорями слушателей в модуле Справочники"""
    class Meta:
        model = audience_category_model
        fields = ['name', ]


class AudienceCategoryListUpdateSerializer(AudienceCategoryBaseSerializer):
    """Сериализация данных при получении списка или обновлении категорий слушателей в модуле Справочники"""
    object_id = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        label='UUID типа ОО'
    )

    class Meta:
        model = audience_category_model
        fields = AudienceCategoryBaseSerializer.Meta.fields + ['object_id']
