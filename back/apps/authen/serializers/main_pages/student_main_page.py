from rest_framework import serializers

from apps.guides.selectors.profiles.student import student_profile_model


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
