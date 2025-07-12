from rest_framework import serializers

from apps.authen.services.profile import profile_service
from apps.edu.selectors.student_group import student_group_model


class ServiceDepartmentSerializer(serializers.ModelSerializer):
    """
    Сериализация данных при получении списка доступных услуг
    для структурного подразделения
    """

    title = serializers.SerializerMethodField(
        label='Наименование услуги'
    )
    date_start = serializers.SerializerMethodField(
        label='Дата начала обучения'
    )
    date_end = serializers.SerializerMethodField(
        label='Дата окончания обучения'
    )
    type = serializers.SerializerMethodField(
        label='Тип'
    )
    duration = serializers.SerializerMethodField(
        label='Объем (часов)'
    )
    curator_fio = serializers.SerializerMethodField(
        label='ФИО куратора'
    )
    curator_email = serializers.SerializerMethodField(
        label='Email куратора'
    )
    curator_phone = serializers.SerializerMethodField(
        label='Телефон куратора'
    )

    def get_title(self, obj):
        if obj.ou:
            if obj.ou.program:
                return obj.ou.program.name
        if obj.iku:
            return obj.iku.name
        return '-'

    def get_date_start(self, obj):
        if obj.ou:
            return obj.ou.date_start.strftime('%d.%m.%Y')
        if obj.iku:
            return obj.iku.date_start.strftime('%d.%m.%Y')
        return '-'

    def get_date_end(self, obj):
        if obj.ou:
            return obj.ou.date_end.strftime('%d.%m.%Y')
        if obj.iku:
            return obj.iku.date_end.strftime('%d.%m.%Y')
        return '-'

    def get_type(self, obj):
        if obj.ou:
            if obj.ou.program:
                return obj.ou.program.type
        if obj.iku:
            if obj.iku.type:
                return obj.iku.type.name
        return '-'

    def get_duration(self, obj):
        if obj.ou:
            if obj.ou.program:
                return obj.ou.program.duration
        if obj.iku:
            return obj.iku.duration
        return 0

    def get_curator_fio(self, obj):
        if obj.curator:
            return profile_service.get_profile_or_info_by_attribute(
                'object_id',
                obj.curator_id,
                'display_name'
            )
        return '-'

    def get_curator_email(self, obj):
        if obj.curator:
            return profile_service.get_profile_or_info_by_attribute(
                'object_id',
                obj.curator_id,
                'email'
            )
        return '-'

    def get_curator_phone(self, obj):
        if obj.curator:
            return profile_service.get_profile_or_info_by_attribute(
                'object_id',
                obj.curator_id,
                'phone'
            )
        return '-'

    class Meta:
        model = student_group_model
        fields = (
            'object_id',
            'title',
            'code',
            'date_start',
            'date_end',
            'type',
            'duration',
            'curator_fio',
            'curator_email',
            'curator_phone'
        )


class ServiceListSerializer(serializers.Serializer):
    """Сериализация данных при получении списка услуг для регистрации"""
    department = serializers.CharField(
        max_length=300,
        allow_null=False,
        allow_blank=False,
        label='Подразделение ЦОКО'
    )
    services = ServiceDepartmentSerializer(
        many=True,
        label='Мероприятия подразделения'
    )
