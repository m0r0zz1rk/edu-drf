from rest_framework import serializers

from apps.applications.selectors.course_application import course_application_model
from apps.applications.serializers.base_application import BaseApplicationSerializer


class FullBaseApplicationSerializer(BaseApplicationSerializer):
    """Расширенный сериализатор для базовых полей заявок обучающихся"""
    region_name = serializers.SerializerMethodField(
        label='Наименование региона РФ'
    )
    region_id = serializers.SerializerMethodField(
        label='object_id региона РФ'
    )
    mo_name = serializers.SerializerMethodField(
        label='Наименование МО (для региона Иркутская область)'
    )
    mo_id = serializers.SerializerMethodField(
        label='object_id МО'
    )
    oo_name = serializers.SerializerMethodField(
        label='Наименование ОО (для региона Иркутская область)'
    )
    oo_id = serializers.SerializerMethodField(
        label='object_id ОО'
    )
    position_category_name = serializers.SerializerMethodField(
        label='Наименование категории должности'
    )
    position_category_id = serializers.SerializerMethodField(
        label='object_id категории должности'
    )
    position_name = serializers.SerializerMethodField(
        label='Наименование должности'
    )
    position_id = serializers.SerializerMethodField(
        label='object_id должности'
    )

    def get_region_name(self, obj):
        if obj.region:
            return obj.region.name
        return '-'

    def get_region_id(self, obj):
        if obj.region:
            return obj.region_id
        return None

    def get_mo_name(self, obj):
        if obj.mo:
            return obj.mo.name
        return '-'

    def get_mo_id(self, obj):
        if obj.mo:
            return obj.mo_id
        return None

    def get_oo_name(self, obj):
        if obj.oo:
            return obj.oo.full_name
        return '-'

    def get_oo_id(self, obj):
        if obj.oo:
            return obj.oo_id
        return None

    def get_position_category_name(self, obj):
        if obj.position_category:
            return obj.position_category.name
        return '-'

    def get_position_category_id(self, obj):
        if obj.position_category:
            return obj.position_category_id
        return None

    def get_position_name(self, obj):
        if obj.position:
            return obj.position.name
        return '-'

    def get_position_id(self, obj):
        if obj.position:
            return obj.position_id
        return None

    class Meta(BaseApplicationSerializer.Meta):
        model = course_application_model
        fields = BaseApplicationSerializer.Meta.fields + (
            'check_survey',
            'work_less',
            'region_name',
            'region_id',
            'mo_name',
            'mo_id',
            'oo_name',
            'oo_id',
            'oo_new',
            'position_category_name',
            'position_category_id',
            'position_name',
            'position_id',
            'physical'
        )