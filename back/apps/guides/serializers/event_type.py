from rest_framework import serializers

from apps.guides.selectors.event_type import event_type_model


class EventTypeBaseSerializer(serializers.ModelSerializer):
    """Базовая сериализация данных при работе с типами мероприятий в модуле Справочники"""
    class Meta:
        model = event_type_model
        fields = ['name', ]


class EventTypeListUpdateSerializer(EventTypeBaseSerializer):
    """Сериализация данных при получении списка муниципальных образований в модуле Справочники"""
    object_id = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label="UUID типа"
    )

    class Meta:
        model = event_type_model
        fields = EventTypeBaseSerializer.Meta.fields + ['object_id', ]
