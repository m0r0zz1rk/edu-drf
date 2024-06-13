from django.apps import apps
from rest_framework import serializers

education_service_model = apps.get_model('edu', 'EducationService')


class BaseServiceSerializer(serializers.ModelSerializer):
    """Сериализация базовых данных об услуги"""
    object_id = serializers.UUIDField(
        allow_null=True,
        label='object_id услуги (при наличии)'
    )
    date_start = serializers.DateField(
        format='%d.%m.%Y',
        label='Дата начала обучения'
    )
    date_end = serializers.DateField(
        format='%d.%m.%Y',
        label='Дата окончания обучения'
    )

    class Meta:
        model = education_service_model
        fields = ('object_id', 'location', 'date_start', 'date_end')

