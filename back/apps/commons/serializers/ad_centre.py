from django.apps import apps
from rest_framework import serializers

ad_centre_model = apps.get_model('commons', 'AdCentre')


class AdCentreSerializer(serializers.ModelSerializer):
    """Сериализация данных для получения списка подразделений-центров из AD"""
    class Meta:
        model = ad_centre_model
        fields = ['object_id', 'display_name']
