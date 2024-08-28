from rest_framework import serializers

from apps.guides.selectors.state import state_model


class StateRegistrationSerializer(serializers.ModelSerializer):
    """Сериализация данных о государстве при регистрации пользователей"""
    class Meta:
        model = state_model
        fields = ('name',)
