from rest_framework import serializers


class PKOneSerializer(serializers.Serializer):
    """
    Сериализация параметров для отчета 1-ПК
    """
    report_year = serializers.IntegerField(
        min_value=2000,
        max_value=3000,
        label='Год'
    )
