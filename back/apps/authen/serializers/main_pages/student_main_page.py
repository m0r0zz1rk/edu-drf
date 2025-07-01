from rest_framework import serializers

from apps.guides.selectors.profiles.student import student_profile_model


class ActiveAppSerializer(serializers.Serializer):
    """Сериализация данных активной заявки пользователя"""
    object_id = serializers.UUIDField(
        allow_null=False,
        label='object_id заявки'
    )
    app_type = serializers.CharField(
        max_length=6,
        allow_null=False,
        allow_blank=False,
        label='Тип заявки'
    )
    name = serializers.CharField(
        max_length=500,
        allow_blank=False,
        allow_null=False,
        label='Наименование услуги'
    )
    status = serializers.CharField(
        max_length=14,
        allow_null=False,
        allow_blank=False,
        label='Статус заявки'
    )


class StudentMainPageSerializer(serializers.ModelSerializer):
    """Сериализация данных обучающегося для главной странице АИС"""
    email = serializers.EmailField(
        allow_null=False,
        allow_blank=False,
        label='Email'
    )
    fio = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label='ФИО'
    )
    active_apps = serializers.ListField(
        child=ActiveAppSerializer(),
        allow_empty=True,
        label='Активные заявки'
    )

    class Meta:
        model = student_profile_model
        fields = [
            'fio',
            'email',
            'phone',
            'snils',
            'active_apps'
        ]
