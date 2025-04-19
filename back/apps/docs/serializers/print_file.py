from rest_framework import serializers


class PrintFileSerializer(serializers.Serializer):
    """
    Сериализация данных при получении запроса на отправку файла печати по почте
    """
    group_id = serializers.UUIDField(
        allow_null=False,
        label='object_id учебной группы'
    )
    to_print_office = serializers.BooleanField(
        label='Параметр отправки файла в типографию'
    )
