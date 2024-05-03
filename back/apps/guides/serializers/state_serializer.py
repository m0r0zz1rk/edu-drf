from django.apps import apps
from rest_framework import serializers

state_model = apps.get_model('guides', 'State')


class StateSerializer(serializers.ModelSerializer):
    """Сериализация данных о государстве"""
    class Meta:
        model = state_model
        fields = ('name',)