from rest_framework import serializers


class ApplicationPayDenySerializer(serializers.Serializer):
    """
    Сериализация при отклоненной оплате
    """
    message = serializers.CharField(
        max_length=500,
        allow_null=False,
        allow_blank=False,
        label='Сообщение пользователю'
    )
