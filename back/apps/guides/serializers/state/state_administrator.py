from rest_framework import serializers

from apps.guides.selectors.state import state_model


class StateAdministratorSerializer(serializers.ModelSerializer):
    """Сериализация данных о государстве для модуля Справочников"""
    class Meta:
        model = state_model
        exclude = ('date_create', )


class StateAdministratorCreateSerializer(serializers.ModelSerializer):
    """Сериализация данных при добавлении государства в модуле Справочники"""
    class Meta:
        model = state_model
        fields = ['name', ]


class StateAdministratorUpdateSerializer(StateAdministratorCreateSerializer):
    """Сериализация данных при редактировании государства в модуле Справочники"""
    object_id = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label='UUID государства'
    )

    class Meta:
        model = state_model
        fields = StateAdministratorCreateSerializer.Meta.fields + ['object_id', ]
