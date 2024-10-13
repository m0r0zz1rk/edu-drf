from rest_framework import serializers

from apps.guides.selectors.region import region_model


class RegionBaseSerializer(serializers.ModelSerializer):
    """Базовая сериалазация данных при работе с регионами РФ"""
    class Meta:
        model = region_model
        fields = ('name', )


class RegionListUpdateSerializer(RegionBaseSerializer):
    """Сериализация данных при получении списка или обновлении регионов РФ"""
    object_id = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        label='UUID региона РФ'
    )

    class Meta(RegionBaseSerializer.Meta):
        model = region_model
        fields = RegionBaseSerializer.Meta.fields + ('object_id', )
