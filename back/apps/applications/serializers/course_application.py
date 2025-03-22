import os

from rest_framework import serializers

from apps.applications.selectors.course_application import course_application_model
from apps.applications.serializers.base_application import (BaseApplicationSerializer,
                                                            FullBaseApplicationSerializer,
                                                            BaseApplicationUpdateSerializer,
                                                            BaseApplicationGroupListSerializer)
from apps.edu.selectors.student_group import student_group_queryset


class CourseApplicationListSerializer(serializers.Serializer):
    """Сериализация данных при получении списка заявок"""
    department = serializers.CharField(
        max_length=300,
        allow_null=False,
        allow_blank=False,
        label='Наименование структурного подразделения'
    )
    apps = BaseApplicationSerializer(
        many=True,
        label='Заявки'
    )


class CourseApplicationDetailSerializer(FullBaseApplicationSerializer):
    """Сериализация данных при получении детальной информации по заявке на курс"""
    education_doc_name = serializers.SerializerMethodField(
        label='Наименование документа об образовании'
    )
    education_doc_object_id = serializers.SerializerMethodField(
        label='object_id документа об образовании'
    )
    profile_surname = serializers.SerializerMethodField(
        label='Фамилия обучающегося из профиля'
    )
    surname_doc_name = serializers.SerializerMethodField(
        label='Наименование документа о смене фамилии'
    )
    surname_doc_object_id = serializers.SerializerMethodField(
        label='object_id документа о смене фамилии'
    )
    education_date = serializers.DateField(
        format='%d.%m.%Y',
        label='Дата выдачи диплома'
    )
    certificate_doc_name = serializers.SerializerMethodField(
        label='Наименование скана удостоверения'
    )
    certificate_doc_object_id = serializers.SerializerMethodField(
        label='object_id скана удостоверения'
    )

    def get_education_doc_name(self, obj):
        if obj.education_doc:
            return os.path.basename(obj.education_doc.file.name)
        return ''

    def get_education_doc_object_id(self, obj):
        if obj.education_doc:
            return obj.education_doc_id
        return None

    def get_profile_surname(self, obj):
        return obj.profile.surname

    def get_surname_doc_name(self, obj):
        if obj.surname_doc:
            return os.path.basename(obj.surname_doc.file.name)
        return ''

    def get_surname_doc_object_id(self, obj):
        if obj.surname_doc:
            return obj.surname_doc_id
        return None

    def get_certificate_doc_name(self, obj):
        if obj.certificate_doc:
            return os.path.basename(obj.certificate_doc.file.name)
        return ''

    def get_certificate_doc_object_id(self, obj):
        if obj.certificate_doc:
            return obj.certificate_doc_id
        return None

    class Meta(FullBaseApplicationSerializer.Meta):
        fields = FullBaseApplicationSerializer.Meta.fields + (
            'education_level',
            'education_category',
            'education_doc_name',
            'education_doc_object_id',
            'education_check',
            'profile_surname',
            'diploma_surname',
            'surname_doc_name',
            'surname_doc_object_id',
            'education_serial',
            'education_number',
            'education_date',
            'certificate_doc_name',
            'certificate_doc_object_id',
            'certificate_mail',
            'mail_address'
        )


class CourseBaseUpdateSerializer(CourseApplicationDetailSerializer):
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
        fields = CourseApplicationDetailSerializer.Meta.fields + (
            'region_object_id',
            'mo_object_id',
            'oo_object_id',
            'position_category_object_id',
            'position_object_id'
        )


class CourseApplicationUpdateSerializer(CourseBaseUpdateSerializer):
    """Сериализация данных при сохранении информации по заявке на курс"""
    education_doc_object_id = serializers.UUIDField(
        allow_null=True,
        label='object_id документа об образовании'
    )
    surname_doc_object_id = serializers.UUIDField(
        allow_null=True,
        label='object_id документа о смене фамилии'
    )
    certificate_doc_object_id = serializers.UUIDField(
        allow_null=True,
        label='object_id скана удостоверения'
    )

    class Meta:
        model = course_application_model
        fields = CourseBaseUpdateSerializer.Meta.fields + (
            'education_doc_object_id',
            'surname_doc_object_id',
            'certificate_doc_object_id'
        )


class CourseAppGroupListSerializer(BaseApplicationGroupListSerializer):
    """Сериализация данных при получении списка заявок для учебной группы"""
    education_doc_name = serializers.SerializerMethodField(
        label='Имя файла документа об образовании'
    )
    pay_doc_name = serializers.SerializerMethodField(
        label='Имя файла документа об оплате'
    )

    def get_education_doc_name(self, obj):
        if obj.education_doc:
            return os.path.basename(obj.education_doc.file.name)
        return ''

    def get_pay_doc_name(self, obj):
        if obj.pay_doc:
            return os.path.basename(obj.pay_doc.file.name)
        return ''

    class Meta:
        model = course_application_model
        fields = (
            'object_id',
            'group',
            'student',
            'date_create',
            'status',
            'oo',
            'oo_new',
            'education_check',
            'education_doc_id',
            'education_doc_name',
            'pay_doc_id',
            'pay_doc_name',
            'check_survey'
        )
