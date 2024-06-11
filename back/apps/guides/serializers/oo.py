from django.apps import apps
from rest_framework import serializers

oo_model = apps.get_model('guides', 'Oo')


class OoBaseSerializer(serializers.ModelSerializer):
    """Базовая сериализация информации при работе с ОО в модуле Справочников"""
    class Meta:
        model = oo_model
        fields = ['short_name', 'full_name', 'form']


class OoListSerializer(OoBaseSerializer):
    """Сериализация данных при получении списка ОО в модуле Справочников"""
    object_id = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label='UUID ОО'
    )
    mo = serializers.SerializerMethodField(label='МО')
    oo_type = serializers.SerializerMethodField(label='Тип ОО')

    def get_mo(self, obj):
        if obj.mo is not None:
            return obj.mo.name
        return '-'

    def get_oo_type(self, obj):
        if obj.oo_type is not None:
            return obj.oo_type.name
        return '-'

    class Meta:
        model = oo_model
        fields = OoBaseSerializer.Meta.fields + ['object_id', 'mo', 'oo_type']


class OoCreateSerializer(OoBaseSerializer):
    """Сериализация данных при добавлении ОО в модуле Справочников"""
    mo = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label='МО'
    )
    oo_type = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label='Тип ОО'
    )

    class Meta:
        model = oo_model
        fields = OoBaseSerializer.Meta.fields + ['mo', 'oo_type']


class OoUpdateSerializer(OoCreateSerializer):
    """Сериализация данных при обновлении ОО в модуле Справочников"""
    object_id = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label='UUID ОО'
    )

    class Meta:
        model = oo_model
        fields = OoCreateSerializer.Meta.fields + ['object_id']
