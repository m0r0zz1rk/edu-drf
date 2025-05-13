from rest_framework import serializers


class DppSerializer(serializers.Serializer):
    """Сериализация данных при получении запроса на формирование отчета ДПП"""
    report_year = serializers.IntegerField(
        min_value=2000,
        max_value=3000,
        label='Год'
    )
    report_month = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label='Месяц (номер или текст "all" для формирования отчета по всему году)'
    )
