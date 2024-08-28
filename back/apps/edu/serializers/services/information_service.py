from rest_framework import serializers

from apps.edu.selectors.services.information_service import information_service_model
from apps.edu.serializers.services.base_service import BaseServiceSerializer


class InformationServiceListSerializer(BaseServiceSerializer):
    """Сериализация данных при получении списка информационно-консультационных услуг (мероприятия)"""
    department = serializers.SerializerMethodField(
        label='Подраздлеление'
    )
    type = serializers.SerializerMethodField(
        label='Тип услуги'
    )

    def get_department(self, obj):
        if obj.department:
            return obj.department.display_name
        return '-'

    def get_type(self, obj):
        if obj.type:
            return obj.type.name
        return '-'

    class Meta:
        model = information_service_model
        exclude = ('date_create', 'duration', 'categories', 'price')


class InformationServiceRetrieveAddUpdateSerializer(BaseServiceSerializer):
    """
        Сериализация данных информационно-консультационной услуги для просмотра (retrieve),
        добавления (create) и обновления (update) объекта
    """
    department = serializers.CharField(
        max_length=300,
        allow_null=False,
        allow_blank=False,
        label='Подразделение'
    )
    type = serializers.CharField(
        max_length=100,
        allow_blank=False,
        allow_null=False,
        label='Тип'
    )
    name = serializers.CharField(
        max_length=300,
        allow_null=False,
        allow_blank=False,
        label='Наименование'
    )
    categories = serializers.CharField(
        max_length=5000,
        allow_null=True,
        allow_blank=True,
        label='Категории слушателей'
    )

    class Meta:
        model = information_service_model
        fields = BaseServiceSerializer.Meta.fields + (
            'department',
            'type',
            'name',
            'categories',
            'duration',
            'price'
        )

