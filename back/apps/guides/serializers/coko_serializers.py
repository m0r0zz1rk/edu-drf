from django.apps import apps
from rest_framework import serializers

coko_profile_model = apps.get_model('authen', 'CokoProfile')


class CokoSerializer(serializers.ModelSerializer):
    """Сериализация данных при выдаче списка сотрудников ЦОКО в модуле Справочники"""
    class Meta:
        model = coko_profile_model
        exclude = ('date_create', 'django_user')


class CokoChangeCuratorGroupsSerializer(serializers.ModelSerializer):
    """Сериализация данных при изменинии отображения кураторских учебных групп у пользователя в модуле Справончики"""
    object_id = serializers.CharField(
        allow_null=False,
        allow_blank=False,
        label='UUID профиля сотрудника'
    )

    class Meta:
        model = coko_profile_model
        fields = ['object_id', 'curator_groups']
