import base64
import os

from rest_framework import serializers

from apps.applications.serializers.base_application import (BaseApplicationSerializer,
                                                            FullBaseApplicationSerializer)


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
    education_doc_file = serializers.SerializerMethodField(
        label='Файл документа об образовании'
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
    surname_doc_file = serializers.SerializerMethodField(
        label='Файл документа о смене фамилии'
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
    certificate_doc_file = serializers.SerializerMethodField(
        label='Файл скана удостоверения'
    )

    def get_education_doc_name(self, obj):
        if obj.education_doc:
            return os.path.basename(obj.education_doc.file.name)
        return ''

    def get_education_doc_object_id(self, obj):
        if obj.education_doc:
            return obj.education_doc_id
        return None

    def get_education_doc_file(self, obj):
        if obj.education_doc:
            try:
                with obj.education_doc.file.open(mode='rb') as doc_file:
                    doc_data = doc_file.read()
                return base64.b64encode(doc_data).decode('utf-8')
            except Exception:
                return None
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

    def get_surname_doc_file(self, obj):
        if obj.surname_doc:
            try:
                with obj.surname_doc.file.open(mode='rb') as doc_file:
                    doc_data = doc_file.read()
                return base64.b64encode(doc_data).decode('utf-8')
            except Exception:
                return None
        return None

    def get_certificate_doc_name(self, obj):
        if obj.certificate_doc:
            return os.path.basename(obj.certificate_doc.file.name)
        return ''

    def get_certificate_doc_object_id(self, obj):
        if obj.certificate_doc:
            return obj.certificate_doc_id
        return None

    def get_certificate_doc_file(self, obj):
        if obj.certificate_doc:
            try:
                with obj.certificate_doc.file.open(mode='rb') as doc_file:
                    doc_data = doc_file.read()
                return base64.b64encode(doc_data).decode('utf-8')
            except Exception:
                return None
        return None

    class Meta(FullBaseApplicationSerializer.Meta):
        fields = FullBaseApplicationSerializer.Meta.fields + (
            'education_level',
            'education_category',
            'education_doc_name',
            'education_doc_object_id',
            'education_doc_file',
            'education_check',
            'profile_surname',
            'diploma_surname',
            'surname_doc_name',
            'surname_doc_object_id',
            'surname_doc_file',
            'education_serial',
            'education_number',
            'education_date',
            'certificate_doc_name',
            'certificate_doc_object_id',
            'certificate_doc_file',
            'certificate_mail',
            'mail_address'
        )


class CourseApplicationUpdateSerializer(CourseApplicationDetailSerializer):
    """Сериализация данных при сохранении информации по заявке на курс"""
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
