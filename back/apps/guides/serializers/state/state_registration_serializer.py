from django.apps import apps
from rest_framework import serializers

state_model = apps.get_model('guides', 'State')


class StateRegistrationSerializer(serializers.ModelSerializer):
    """Сериализация данных о государстве при регистрации пользователей"""
    class Meta:
        model = state_model
        fields = ('name',)
