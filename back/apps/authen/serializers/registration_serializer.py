from django.core.validators import MinLengthValidator
from rest_framework import serializers

from apps.authen.models import Profiles


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор данных для регистрации пользователя"""
    email = serializers.EmailField()
    role = serializers.CharField(max_length=20)
    password = serializers.CharField(
        validators=[MinLengthValidator(8, 'Минимальная длина пароля - 8 символов'), ]
    )

    class Meta:
        model = Profiles
        fields = [
            'state',
            'surname',
            'name',
            'patronymic',
            'sex',
            'birthday',
            'phone',
            'email',
            'role',
            'oo_shortname',
            'oo_fullname',
            'password'
        ]


class RegistrationUniquePhoneSerializer(serializers.Serializer):
    """Сериализация номера телефона"""
    phone = serializers.CharField(
        min_length=18,
        max_length=18,
        label='Телефон'
    )


class RegistrationUniqueEmailSerializer(serializers.Serializer):
    """Сериализация email"""
    email = serializers.EmailField(
        allow_null=False,
        allow_blank=False,
        label='Email'
    )
