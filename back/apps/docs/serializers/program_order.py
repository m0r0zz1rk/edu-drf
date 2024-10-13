from rest_framework import serializers

from apps.docs.selectors.program_order import program_order_model


class ProgramOrderBaseSerializer(serializers.ModelSerializer):
    """Базовая сериализация данных для приказов ДПП"""
    class Meta:
        model = program_order_model
        fields = ['number', 'date', 'file']
