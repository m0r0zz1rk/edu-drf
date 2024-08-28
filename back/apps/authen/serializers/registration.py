from django.core.validators import MinLengthValidator
from rest_framework import serializers

from apps.guides.selectors.state import state_model
from apps.guides.selectors.user import student_profile_model


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор данных для регистрации пользователя"""
    email = serializers.EmailField(label='Email')
    password = serializers.CharField(
        validators=[MinLengthValidator(8, 'Минимальная длина пароля - 8 символов'), ],
        label='Пароль'
    )
    state = serializers.SlugRelatedField(slug_field='name', queryset=state_model.objects.all())

    class Meta:
        model = student_profile_model
        fields = [
            'surname',
            'name',
            'patronymic',
            'phone',
            'email',
            'snils',
            'state',
            'birthday',
            'sex',
            'health',
            'password'
        ]


class RegistrationUniquePhoneSerializer(serializers.Serializer):
    """Сериализация номера телефона"""
    phone = serializers.CharField(
        min_length=18,
        max_length=18,
        label='Телефон'
    )


class RegistrationUniqueSnilsSerializer(serializers.Serializer):
    """Сериализация номера телефона"""
    snils = serializers.CharField(
        min_length=14,
        max_length=14,
        label='СНИЛС'
    )


class RegistrationUniqueEmailSerializer(serializers.Serializer):
    """Сериализация email"""
    email = serializers.EmailField(
        allow_null=False,
        allow_blank=False,
        label='Email'
    )
