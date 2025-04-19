from rest_framework import serializers


class ApplicationOOUpdateSerializer(serializers.Serializer):
    """
    Сериализация при подтверждении проверки ОО в заявке
    """
    oo_new = serializers.CharField(
        allow_blank=True,
        allow_null=False,
        label='Наименование нового ОО'
    )
    oo_id = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label='object_id выбранной организации'
    )
