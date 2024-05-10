from django.apps import apps
from rest_framework import serializers

student_profile_model = apps.get_model('authen', 'StudentProfile')

states_model = apps.get_model('guides', 'State')

class BaseProfileSerializer(serializers.ModelSerializer):
    """Базовая сериализация данных профиля пользователя"""
    state = serializers.SlugRelatedField(
        slug_field='name',
        queryset=states_model.objects.all(),
        label='Государство'
    )
    email = serializers.SerializerMethodField(label='Email')

    def get_email(self, obj):
        """Получение Email из объекта User"""
        return obj['django_user']['email']

    class Meta:
        model = student_profile_model
        fields = [
            'surname',
            'email',
            'name',
            'patronymic',
            'phone',
            'snils',
            'state',
            'birthday',
            'sex',
            'health'
        ]


class ProfileInputSerializer(BaseProfileSerializer):
    """Сериализация данных профиля пользователя при получении из request"""
    phone = serializers.CharField(
        max_length=18,
        allow_null=False,
        allow_blank=False,
        label='Телефон'
    )
    snils = serializers.CharField(
        max_length=14,
        allow_null=False,
        allow_blank=False,
        label='СНИЛС'
    )
    email = serializers.EmailField(label='Email')


class ProfileOutputSerializer(BaseProfileSerializer):
    """Сериализация данных профиля пользователя при выдаче"""
    email = serializers.SerializerMethodField(label='Email')
    birthday = serializers.DateField(format='%d.%m.%Y')

    def get_email(self, obj):
        return obj.django_user.email


class ProfileChangePasswordSerializer(serializers.Serializer):
    """Сериализация данных при смене пароля пользователя"""
    password = serializers.CharField(
        min_length=8,
        allow_blank=False,
        allow_null=False,
        label='Пароль'
    )



