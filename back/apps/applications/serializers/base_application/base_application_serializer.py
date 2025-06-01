from rest_framework import serializers

from apps.applications.selectors.course_application import course_application_model


class BaseApplicationSerializer(serializers.ModelSerializer):
    """Сериализация полей базовой модели заявок обучающихся"""
    date_create = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        label='Дата создания заявки'
    )
    group_code = serializers.SerializerMethodField(
        label='Шифр группы'
    )
    department = serializers.SerializerMethodField(
        label='Структурное подразделение, проводящее услугу'
    )
    service_type = serializers.SerializerMethodField(
        label='Тип услуги'
    )
    service_title = serializers.SerializerMethodField(
        label='Наименование услуги'
    )
    service_duration = serializers.SerializerMethodField(
        label='Объем услуги (часов)'
    )
    service_date_range = serializers.SerializerMethodField(
        label='Сроки проведения услуги'
    )
    curator_display_name = serializers.SerializerMethodField(
        label='ФИО куратора группы'
    )
    curator_phone = serializers.SerializerMethodField(
        label='Телефон куратора группы'
    )
    curator_email = serializers.SerializerMethodField(
        label='Email куратора группы'
    )

    def get_service_type(self, obj):
        if obj.group.ou:
            if obj.group.ou.program:
                return obj.group.ou.program.type
        if obj.group.iku:
            if obj.group.iku.type:
                return obj.group.iku.type.name
        return '-'

    def get_group_code(self, obj):
        return obj.group.code

    def get_department(self, obj):
        if obj.group.ou:
            if obj.group.ou.program:
                return obj.group.ou.program.department.display_name
        if obj.group.iku:
            return obj.group.iku.department.display_name
        return '-'

    def get_service_title(self, obj):
        if obj.group.ou:
            if obj.group.ou.program:
                return obj.group.ou.program.name
        if obj.group.iku:
            return obj.group.iku.name
        return '-'

    def get_service_duration(self, obj):
        if obj.group.ou:
            if obj.group.ou.program:
                return obj.group.ou.program.duration
        if obj.group.iku:
            return obj.group.iku.duration
        return 0

    def get_service_date_range(self, obj):
        if obj.group.ou:
            return (f'{obj.group.ou.date_start.strftime("%d.%m.%Y")} - '
                    f'{obj.group.ou.date_end.strftime("%d.%m.%Y")}')
        if obj.group.iku:
            return (f'{obj.group.iku.date_start.strftime("%d.%m.%Y")} - '
                    f'{obj.group.iku.date_end.strftime("%d.%m.%Y")}')
        return '-'

    def get_curator_display_name(self, obj):
        if obj.group.curator:
            return obj.group.curator.display_name
        return '-'

    def get_curator_phone(self, obj):
        if obj.group.curator:
            return obj.group.curator.internal_phone
        return '-'

    def get_curator_email(self, obj):
        if obj.group.curator:
            return obj.group.curator.django_user.email
        return '-'

    class Meta:
        model = course_application_model
        fields = (
            'object_id',
            'profile_id',
            'date_create',
            'group_code',
            'department',
            'curator_display_name',
            'curator_phone',
            'curator_email',
            'service_title',
            'service_type',
            'service_duration',
            'service_date_range',
            'status',
        )
