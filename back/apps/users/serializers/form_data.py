from rest_framework import serializers


class RecFormDataSerializer(serializers.Serializer):
    """
    Сериализация одной записи для массива данных, необходимых для заполнения
    анкеты в заявках обучающегося
    """
    object_id = serializers.UUIDField(
        allow_null=False,
        label='object_id объекта'
    )
    name = serializers.CharField(
        max_length=500,
        allow_null=False,
        allow_blank=False,
        label='Наименование объекта'
    )


class FormDataSerializer(serializers.Serializer):
    """
    Сериализация массива данных, необходимых для заполнения анкеты
    в заявке обучающегося
    """
    region = RecFormDataSerializer(
        many=True,
        label='Регионы РФ'
    )
    mo = RecFormDataSerializer(
        many=True,
        label='МО'
    )
    position_category = RecFormDataSerializer(
        many=True,
        label='Категории должностей'
    )
    position = RecFormDataSerializer(
        many=True,
        label='Должности'
    )
