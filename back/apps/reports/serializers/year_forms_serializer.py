from rest_framework import serializers


class YearFormsSerializer(serializers.Serializer):
    """
    Сериализация параметров для выгрузки анкет за год
    """
    report_year = serializers.IntegerField(
        min_value=2000,
        max_value=3000,
        label='Год'
    )
    service_type = serializers.CharField(
        max_length=3,
        allow_null=False,
        allow_blank=False,
        label='Тип услуги (ou или iku)'
    )
