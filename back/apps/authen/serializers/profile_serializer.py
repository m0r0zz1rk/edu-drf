from rest_framework import serializers

from apps.authen.models import Profiles


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор данных профиля пользователя"""
    state = serializers.CharField(max_length=200)
    email = serializers.EmailField(label='Email')
    role = serializers.CharField(
        max_length=30,
        label='Роль пользователя'
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
            'age',
            'oo_shortname',
            'oo_fullname',
            'phone',
            'email',
            'role'
        ]


class ProfileChangePasswordSerializer(serializers.Serializer):
    """Сериализация данных при смене пароля пользователя"""
    password = serializers.CharField(
        min_length=8,
        label='Пароль'
    )



