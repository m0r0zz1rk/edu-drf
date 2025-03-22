from rest_framework import serializers

from apps.applications.selectors.course_application import course_application_model
from apps.applications.selectors.event_application import event_application_model
from apps.edu.selectors.student_group import student_group_queryset


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


class FullBaseApplicationSerializer(BaseApplicationSerializer):
    """Расширенный сериализатор для базовых полей заявок обучающихся"""
    study_url = serializers.SerializerMethodField(
        label='Ссылка на обучение'
    )
    region_name = serializers.SerializerMethodField(
        label='Наименование региона РФ'
    )
    region_object_id = serializers.SerializerMethodField(
        label='object_id региона РФ'
    )
    mo_name = serializers.SerializerMethodField(
        label='Наименование МО (для региона Иркутская область)'
    )
    mo_object_id = serializers.SerializerMethodField(
        label='object_id МО'
    )
    oo_name = serializers.SerializerMethodField(
        label='Наименование ОО (для региона Иркутская область)'
    )
    oo_object_id = serializers.SerializerMethodField(
        label='object_id ОО'
    )
    position_category_name = serializers.SerializerMethodField(
        label='Наименование категории должности'
    )
    position_category_object_id = serializers.SerializerMethodField(
        label='object_id категории должности'
    )
    position_name = serializers.SerializerMethodField(
        label='Наименование должности'
    )
    position_object_id = serializers.SerializerMethodField(
        label='object_id должности'
    )

    def get_study_url(self, obj):
        return obj.group.event_url

    def get_region_name(self, obj):
        if obj.region:
            return obj.region.name
        return '-'

    def get_region_object_id(self, obj):
        if obj.region:
            return obj.region_id
        return None

    def get_mo_name(self, obj):
        if obj.mo:
            return obj.mo.name
        return '-'

    def get_mo_object_id(self, obj):
        if obj.mo:
            return obj.mo_id
        return None

    def get_oo_name(self, obj):
        if obj.oo:
            return obj.oo.full_name
        return '-'

    def get_oo_object_id(self, obj):
        if obj.oo:
            return obj.oo_id
        return None

    def get_position_category_name(self, obj):
        if obj.position_category:
            return obj.position_category.name
        return '-'

    def get_position_category_object_id(self, obj):
        if obj.position_category:
            return obj.position_category_id
        return None

    def get_position_name(self, obj):
        if obj.position:
            return obj.position.name
        return '-'

    def get_position_object_id(self, obj):
        if obj.position:
            return obj.position_id
        return None

    class Meta(BaseApplicationSerializer.Meta):
        model = course_application_model
        fields = BaseApplicationSerializer.Meta.fields + (
            'study_url',
            'check_survey',
            'work_less',
            'region_name',
            'region_object_id',
            'mo_name',
            'mo_object_id',
            'oo_name',
            'oo_object_id',
            'oo_new',
            'position_category_name',
            'position_category_object_id',
            'position_name',
            'position_object_id',
            'physical'
        )


class RequestApplicationCreateSerializer(serializers.Serializer):
    """Сериализация данных при запросе на создании заявки"""
    group_id = serializers.UUIDField(
        allow_null=False,
        label='object_id учебной группы'
    )


class ResponseApplicationCreateSerializer(serializers.Serializer):
    """Сериализация данных ответа на запроса на создание заявки"""
    app_id = serializers.UUIDField(
        allow_null=False,
        label='object_id созданной заявки'
    )


class BaseApplicationUpdateSerializer(serializers.Serializer):
    """Базовый сериалайзер для обновления заявки обучающегося"""
    region_object_id = serializers.UUIDField(
        allow_null=False,
        label='object_id региона РФ'
    )
    mo_object_id = serializers.UUIDField(
        allow_null=True,
        label='object_id МО (для региона Иркутская область)'
    )
    oo_object_id = serializers.UUIDField(
        allow_null=True,
        label='object_id ОО из справочника'
    )
    position_category_object_id = serializers.UUIDField(
        allow_null=True,
        label='object_id категории должности'
    )
    position_object_id = serializers.UUIDField(
        allow_null=True,
        label='object_id должности'
    )

    class Meta:
        model = course_application_model
        fields = (
            'region_object_id',
            'mo_object_id',
            'oo_object_id',
            'position_category_object_id',
            'position_object_id'
        )


class BaseApplicationGroupListSerializer(serializers.ModelSerializer):
    """Сериализация данных при получении списка заявок для учебной группы"""
    group = serializers.SlugRelatedField(
        slug_field='code',
        queryset=student_group_queryset,
        label='Учебная группа'
    )
    student = serializers.SerializerMethodField(
        label='Информация об обучающемся'
    )
    date_create = serializers.DateTimeField(
        format='%d.%m.%Y',
        label='Дата подачи заявки'
    )

    def get_student(self, obj):
        return {
            'display_name': obj.profile.display_name,
            'email': obj.profile.django_user.email,
            'phone': obj.profile.phone,
        }

    class Meta:
        model = event_application_model
        fields = (
            'object_id',
            'group',
            'student',
            'date_create',
            'status',
            'oo',
            'oo_new',
            'check_survey'
        )
