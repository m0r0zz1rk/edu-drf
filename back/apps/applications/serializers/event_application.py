from rest_framework import serializers

from apps.applications.selectors.event_application import event_application_model
from apps.applications.serializers.base_application import BaseApplicationSerializer, FullBaseApplicationSerializer, \
    BaseApplicationGroupListSerializer


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
    region_id = serializers.UUIDField(
        allow_null=False,
        label='object_id региона РФ'
    )
    mo_id = serializers.UUIDField(
        allow_null=True,
        label='object_id МО (для региона Иркутская область)'
    )
    oo_id = serializers.UUIDField(
        allow_null=True,
        label='object_id ОО из справочника'
    )
    position_category_id = serializers.UUIDField(
        allow_null=True,
        label='object_id категории должности'
    )
    position_id = serializers.UUIDField(
        allow_null=True,
        label='object_id должности'
    )
    in_work = serializers.BooleanField(
        allow_null=False,
        default=False,
        label='Установить статус "В работе"'
    )

    class Meta:
        model = event_application_model
        fields = EventApplicationDetailSerializer.Meta.fields + (
            'region_id',
            'mo_id',
            'oo_id',
            'position_category_id',
            'position_id',
            'in_work'
        )


class EventApplicationGroupListSerializer(BaseApplicationGroupListSerializer):
    """Сериализация данных при получении списка заявок для учебной группы"""
    pass
