from rest_framework import serializers
from apps.commons.services.ad.ad_centre_coko_user import AdCentreCokoUserUtils
from apps.guides.selectors.coko import coko_profile_model


class CokoSerializer(serializers.ModelSerializer):
    """Сериализация данных при выдаче списка сотрудников ЦОКО в модуле Справочники"""
    department = serializers.SerializerMethodField(
        label='Подразделение'
    )

    def get_department(self, obj):
        """Получение подразделения-центра AD для пользователя"""
        return AdCentreCokoUserUtils().get_user_centre_display_name(obj.django_user)

    class Meta:
        model = coko_profile_model
        fields = ['object_id', 'surname', 'name', 'patronymic', 'department', 'curator_groups']


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
