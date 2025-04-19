from rest_framework import serializers

from apps.applications.services.base_application import base_application_service
from apps.edu.consts.student_group.doc_types import STUDENT_GROUP_DOC_TYPES
from apps.edu.selectors.student_group import student_group_model


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
            return obj.ou.program.name
        else:
            return obj.iku.name

    def get_date_start(self, obj):
        if obj.ou:
            return obj.ou.date_start.strftime('%d.%m.%Y')
        else:
            return obj.iku.date_start.strftime('%d.%m.%Y')

    def get_date_end(self, obj):
        if obj.ou:
            return obj.ou.date_end.strftime('%d.%m.%Y')
        else:
            return obj.iku.date_end.strftime('%d.%m.%Y')

    def get_curator(self, obj):
        if obj.curator:
            return obj.curator.display_name
        return '-'

    def get_apps_count(self, obj):
        return base_application_service.get_app_count_for_group(
            obj.object_id,
            obj.ou
        )

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
            'form',
            'date_enroll',
            'date_exp',
            'enroll_number',
            'exp_number'
        )


class StudentGroupRetrieveSerializer(StudentGroupListSerializer):
    """
    Сериализация данных при получении информации по конкретной группе
    """
    check_data = serializers.SerializerMethodField(label='Данные для проверки')
    service_type = serializers.SerializerMethodField(label='Тип услуги')

    def get_check_data(self, obj):
        return base_application_service.get_check_data(obj.object_id)

    def get_service_type(self, obj):
        return 'ou' if obj.ou else 'iku'

    class Meta:
        model = StudentGroupListSerializer.Meta.model
        fields = StudentGroupListSerializer.Meta.fields + ('check_data', 'service_type')


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


class StudentGroupBaseDocRequestSerializer(serializers.Serializer):
    group_id = serializers.UUIDField(
        allow_null=False,
        label='object_id учебной группы'
    )


class StudentGroupDocRequestSerializer(StudentGroupBaseDocRequestSerializer):
    doc_type = serializers.ChoiceField(
        choices=STUDENT_GROUP_DOC_TYPES,
        label='Тип запрашиваемого документа'
    )


class StudentGroupCertListSerializer(StudentGroupDocRequestSerializer):
    """
    Сериализация данных для получения ведомости удостоверений учебной группы
    """
    enroll_number = serializers.CharField(
        max_length=50,
        allow_null=False,
        allow_blank=False,
        label='Номер приказа о зачислении'
    )
    enroll_date = serializers.DateField(
        format='%d.%m.%Y',
        allow_null=False,
        label='Дата приказа о зачислении'
    )
    exp_number = serializers.CharField(
        max_length=50,
        allow_null=False,
        allow_blank=False,
        label='Номер приказа об отчислении'
    )
    exp_date = serializers.DateField(
        format='%d.%m.%Y',
        allow_null=False,
        label='Дата приказа об отчислении'
    )
