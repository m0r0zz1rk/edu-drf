from rest_framework import serializers

from apps.applications.selectors.event_application import event_application_model
from apps.applications.serializers.base_application import BaseApplicationSerializer, FullBaseApplicationSerializer, \
    BaseApplicationUpdateSerializer, BaseApplicationGroupListSerializer


class EventApplicationListSerializer(serializers.Serializer):
    """Сериализация данных при получении списка заявок"""
    department = serializers.CharField(
        max_length=300,
        allow_null=False,
        allow_blank=False,
        label='Наименование структурного подразделения'
    )
    apps = BaseApplicationSerializer(
        many=True,
        label='Заявки'
    )


class EventApplicationDetailSerializer(FullBaseApplicationSerializer):
    """Сериализация данных при получении детальной информации по заявке на курс"""
    pass


class EventApplicationUpdateSerializer(EventApplicationDetailSerializer):
    region_object_id = serializers.UUIDField(
        allow_null=False,
        label='object_id региона РФ'
    )
    mo_object_id = serializers.UUIDField(
        allow_null=True,
        label='object_id МО (для региона Иркутская область)'
    )
    oo_object_id = serializers.UUIDField(
        allow_null=True,
        label='object_id ОО из справочника'
    )
    position_category_object_id = serializers.UUIDField(
        allow_null=True,
        label='object_id категории должности'
    )
    position_object_id = serializers.UUIDField(
        allow_null=True,
        label='object_id должности'
    )

    class Meta:
        model = event_application_model
        fields = EventApplicationDetailSerializer.Meta.fields + (
            'region_object_id',
            'mo_object_id',
            'oo_object_id',
            'position_category_object_id',
            'position_object_id'
        )


class EventApplicationGroupListSerializer(BaseApplicationGroupListSerializer):
    """Сериализация данных при получении списка заявок для учебной группы"""
    pass
