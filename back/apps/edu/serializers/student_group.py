from rest_framework import serializers

from apps.authen.services.profile import ProfileService
from apps.edu.selectors.student_group import student_group_model
from apps.edu.services.service.education_service import EducationServiceService
from apps.edu.services.service.information_service import InformationServiceService


class StudentGroupListSerializer(serializers.ModelSerializer):
    """Сериализация данных при получении списка"""
    service_name = serializers.SerializerMethodField(
        label='Наименование услуги'
    )
    date_start = serializers.SerializerMethodField(
        label='Дата начала оказания услуги'
    )
    date_end = serializers.SerializerMethodField(
        label='Дата начала оказания услуги'
    )
    curator = serializers.SerializerMethodField(
        label='Куратор'
    )
    apps_count = serializers.SerializerMethodField(
        label='Количество заявок'
    )

    def get_service_name(self, obj):
        if obj.ou:
            return EducationServiceService().get_info_by_service(
                'object_id',
                obj.ou.object_id,
                'service_name'
            )
        else:
            return InformationServiceService().get_info_by_service(
                'object_id',
                obj.iku.object_id,
                'service_name'
            )

    def get_date_start(self, obj):
        if obj.ou:
            return EducationServiceService().get_info_by_service(
                'object_id',
                obj.ou.object_id,
                'date_start'
            )
        else:
            return InformationServiceService().get_info_by_service(
                'object_id',
                obj.iku.object_id,
                'date_start'
            )

    def get_date_end(self, obj):
        if obj.ou:
            return EducationServiceService().get_info_by_service(
                'object_id',
                obj.ou.object_id,
                'date_end'
            )
        else:
            return InformationServiceService().get_info_by_service(
                'object_id',
                obj.iku.object_id,
                'date_end'
            )

    def get_curator(self, obj):
        if obj.curator:
            return ProfileService().get_profile_or_info_by_attribute(
                'object_id',
                obj.curator_id,
                'display_name'
            )
        return '-'

    def get_apps_count(self, obj):
        return 0

    class Meta:
        model = student_group_model
        fields = (
            'object_id',
            'code',
            'service_name',
            'date_start',
            'date_end',
            'curator',
            'curator_id',
            'apps_count',
            'status',
            'event_url',
            'plan_seats_number',
            'form'
        )


class StudentGroupAddSerializer(serializers.Serializer):
    """Сериализация данных для добавления новой учебной группы"""
    type = serializers.CharField(
        max_length=3,
        allow_null=False,
        allow_blank=False,
        label='Тип услуги (ou/iku)'
    )
    service_id = serializers.UUIDField(
        allow_null=False,
        label='object_id услуги'
    )
    plan_seats_number = serializers.IntegerField(
        min_value=0,
        allow_null=False,
        label='Плановое количество мест (для ИКУ)'
    )


class StudentGroupServiceTypeSerializer(serializers.Serializer):
    """Сериализация данных при получении типа услуги учебной группы"""
    service_type = serializers.CharField(
        max_length=3,
        allow_null=False,
        allow_blank=False,
        label='Тип услуги (ou/iku)'
    )


class StudentGroupUpdateSerializer(serializers.Serializer):
    """Сериализация данных при обновлении информации по учебной группе"""
    code = serializers.CharField(
        max_length=50,
        allow_null=False,
        allow_blank=False,
        label='Шифр'
    )
    curator_id = serializers.UUIDField(
        allow_null=True,
        label='object_id профиля пользователя ЦОКО'
    )
    status = serializers.CharField(
        max_length=30,
        allow_null=False,
        allow_blank=False,
        label='Статус учебной группы'
    )
    form = serializers.CharField(
        max_length=10,
        allow_null=False,
        allow_blank=False,
        label='Форма обучения'
    )
    plan_seats_number = serializers.IntegerField(
        min_value=0,
        allow_null=True,
        label='Плановое количество мест'
    )
