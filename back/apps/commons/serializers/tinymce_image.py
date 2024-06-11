from rest_framework import serializers


class TinyMCEImageSerializer(serializers.Serializer):
    """Серализация данных при загрузке изображений в TinyMCE"""
    name = serializers.CharField(
        max_length=100,
        label='Имя'
    )
    file = serializers.FileField()
