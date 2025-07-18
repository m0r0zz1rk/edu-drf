from rest_framework import serializers

from apps.commons.drf.base64_coko_file_field import Base64CokoFileField


class PayDocSerializer(serializers.Serializer):
    """Сериализация данных для документа об образовании"""
    profile_id = serializers.UUIDField(
        allow_null=False,
        label='object_id профиля пользователя'
    )
    app_id = serializers.UUIDField(
        allow_null=False,
        label='object_id заявки пользователя'
    )
    file = Base64CokoFileField(
        required=True,
        allow_null=False,
        label='Документ об оплате'
    )
