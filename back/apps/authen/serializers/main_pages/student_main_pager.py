from django.apps import apps
from rest_framework import serializers

student_profile_model = apps.get_model('authen', 'StudentProfile')


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

    class Meta:
        model = student_profile_model
        fields = [
            'fio',
            'email',
            'phone',
            'snils'
        ]
