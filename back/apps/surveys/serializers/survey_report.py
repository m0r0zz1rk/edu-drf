from rest_framework import serializers


class ReportParametersSerializer(serializers.Serializer):
    """
    Сериализация параметров отчета по опросу
    """
    survey_id = serializers.UUIDField(
        allow_null=False,
        label='object_id опроса в БД'
    )
    type = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label='Тип отчета (all, group или service_type)'
    )
    start_period = serializers.DateField(
        format='%d.%m.%Y',
        allow_null=False,
        label='Дата начала периода ответов'
    )
    end_period = serializers.DateField(
        format='%d.%m.%Y',
        allow_null=False,
        label='Дата окончания периода ответов'
    )
    group_id = serializers.UUIDField(
        allow_null=True,
        label='object_id выбранной учебной группы'
    )
    service_type = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label='Тип услуги (edu или iku)'
    )
