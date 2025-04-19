from rest_framework import serializers


class StudentGroupOfferSerializer(serializers.Serializer):
    """
    Сериализатор для обновления договора оферты в учебной группе
    """
    file = serializers.FileField(
        label='Скан договора оферты (PDF)'
    )
