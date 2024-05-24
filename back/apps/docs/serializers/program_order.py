from django.apps import apps
from rest_framework import serializers

program_order_model = apps.get_models('docs', 'ProgramOrder')


class ProgramOrderBaseSerializer(serializers.ModelSerializer):
    """Базовая сериализация данных для приказов ДПП"""
    class Meta:
        model = program_order_model
        fields = ['number', 'date', 'file']
