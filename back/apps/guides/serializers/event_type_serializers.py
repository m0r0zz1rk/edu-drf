from django.apps import apps
from rest_framework import serializers

event_type_model = apps.get_model('guides', 'EventType')


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
        label="UUID МО"
    )

    class Meta:
        model = event_type_model
        fields = EventTypeBaseSerializer.Meta.fields + ['object_id', ]
