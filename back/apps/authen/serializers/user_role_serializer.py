from rest_framework import serializers


class UserRoleSerializer(serializers.Serializer):
    """Сериализация для ответа на запрос на получение роли пользователя"""
    role = serializers.CharField(
        max_length=7,
        allow_null=False,
        allow_blank=False,
        label='Роль пользователя'
    )
