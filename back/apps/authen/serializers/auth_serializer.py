from rest_framework import serializers


class AuthSerializer(serializers.Serializer):
    """Сериализация данных для авторизации пользователя"""
    login = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label='Имя пользователя (логин, телефон или email)'
    )
    password = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        label='Пароль'
    )
    centre_auth = serializers.BooleanField(
        label='Авторизация сотрудника организации'
    )


class AuthorizationResponseSerializer(serializers.Serializer):
    """Сериализация данных при успешной авторизации"""
    coko_token = serializers.CharField(
        max_length=2048,
        allow_blank=False,
        allow_null=False,
        label='JWT-токен пользователя'
    )
    coko_user_id = serializers.IntegerField(
        label='ID пользователя'
    )
