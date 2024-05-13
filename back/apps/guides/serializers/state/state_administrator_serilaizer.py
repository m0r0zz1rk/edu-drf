from django.apps import apps
from rest_framework import serializers

state_model = apps.get_model(app_label='guides', model_name='State')


class StateAdministratorSerializer(serializers.ModelSerializer):
    """Сериализация данных о государстве для модуля Справочников"""
    class Meta:
        model = state_model
        exclude = ('date_create', )
