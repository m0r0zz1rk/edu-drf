from django.apps import apps
from rest_framework import serializers

from apps.authen.serializers.profile_serializer import ProfileOutputSerializer

profile_model = apps.get_model('authen', 'StudentProfile')


class UserSerializer(ProfileOutputSerializer):
    """Сериализация данных пользователя для получения списка в модуле Сравочников"""
    date_create = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        label='Дата регистрации'
    )
    teacher = serializers.BooleanField(
        label='Пользователь является преподавателем'
    )

    class Meta:
        model = profile_model
        fields = ProfileOutputSerializer.Meta.fields + ['teacher', 'date_create']
