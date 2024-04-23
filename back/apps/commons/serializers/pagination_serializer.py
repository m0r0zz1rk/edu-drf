from django.core.validators import MinValueValidator
from rest_framework import serializers


class PaginationSerializer(serializers.Serializer):
    """Сериализация пагинационных данных для полученного ModelSerializer"""

    count = serializers.IntegerField(
        validators=[MinValueValidator(0),]
    )
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    total_average_price = serializers.IntegerField(
        validators=[MinValueValidator(0),]
    )
