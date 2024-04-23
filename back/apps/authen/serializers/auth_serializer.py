from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    """Сериализатор для входа в систему"""
    username = serializers.CharField()
    password = serializers.CharField()


class AuthorizationResponseSerializer(serializers.Serializer):
    """Сериализатор ответа системы в случае успешной авторизации"""
    iohk_token = serializers.CharField(
        max_length=2048,
        allow_blank=False,
        allow_null=False
    )
    iohk_user_id = serializers.IntegerField()