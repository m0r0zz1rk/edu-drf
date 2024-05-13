from django.apps import apps
from rest_framework import serializers

from apps.authen.serializers.profile_serializer import ProfileOutputSerializer, ProfileInputSerializer, \
    ProfileChangePasswordSerializer

profile_model = apps.get_model('authen', 'StudentProfile')


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя для получения списка в модуле Сравочников"""
    date_create = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        label='Дата регистрации'
    )
    email = serializers.SerializerMethodField(label='Email')

    def get_email(self, obj):
        return obj.django_user.email

    class Meta:
        model = profile_model
        fields = [
            'object_id',
            'date_create',
            'surname',
            'name',
            'patronymic',
            'snils',
            'phone',
            'email'
        ]


class UserRetrieveSerializer(ProfileOutputSerializer):
    """Сериализация данных о пользователе при посмотре через модуль Справочников"""
    teacher = serializers.BooleanField(label='Является преподавателем')

    class Meta:
        model = profile_model
        fields = ProfileOutputSerializer.Meta.fields + ['teacher', ]


class UserUpdateSerializer(ProfileInputSerializer):
    """Сериализация данных о пользователе при обнолвении информации через модуль Справочников"""
    object_id = serializers.UUIDField(
        allow_null=False,
        label='UUID профиля'
    )
    teacher = serializers.BooleanField(label='Является преподавателем')

    class Meta:
        model = profile_model
        fields = ProfileOutputSerializer.Meta.fields + ['teacher', 'object_id']


class BaseUserUniqueDataSerializer(serializers.Serializer):
    """Сериализация ID профиля при проверке уникальности данных пользователя в модуле Справочников"""
    profile_id = serializers.UUIDField(
        allow_null=False,
        label='ID профиля пользователя'
    )


class UserUniquePhoneSerializer(BaseUserUniqueDataSerializer):
    """Сериализация данных при проверке уникальности номера телефона пользователя в модуле Справочников"""
    phone = serializers.CharField(
        min_length=18,
        max_length=18,
        label='Телефон'
    )


class UserUniqueSnilsSerializer(BaseUserUniqueDataSerializer):
    """Сериализация данных при проверке уникальности номера телефона пользователя в модуле Справочников"""
    snils = serializers.CharField(
        min_length=14,
        max_length=14,
        label='СНИЛС'
    )


class UserUniqueEmailSerializer(BaseUserUniqueDataSerializer):
    """Сериализация данных при проверке уникальности номера телефона пользователя в модуле Справочников"""
    email = serializers.EmailField(
        allow_null=False,
        allow_blank=False,
        label='Email'
    )


class UserChangePasswordSerializer(ProfileChangePasswordSerializer):
    """Сериализация данных при смене пароля пользователя в модуле Справочников"""
    profile_id = serializers.UUIDField(
        allow_null=False,
        label='UUID профиля пользователя'
    )
