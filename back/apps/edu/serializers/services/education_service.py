from rest_framework import serializers

from apps.edu.selectors.services.education_service import education_service_model
from apps.edu.serializers.program import ProgramEducationServiceSerializer
from apps.edu.serializers.services.base_service import BaseServiceSerializer


class EducationServiceBaseSerializer(BaseServiceSerializer):
    """Сериализация базовых данных при работе с образовательной услугой (курсом)"""

    def get_program(self, obj):
        """Получение наименование программы"""
        if obj.program:
            return obj.program.name
        return '-'

    class Meta:
        model = education_service_model
        exclude = ('date_create',)


class EducationServiceListSerializer(EducationServiceBaseSerializer):
    """Сериализация данных при получении списка образовательных услуг (курсов)"""
    program = serializers.SerializerMethodField(
        label='Наименование ДПП'
    )

    def get_program(self, obj):
        """Получение наименование программы"""
        if obj.program:
            return obj.program.name
        return '-'


class EducationServiceRetrieveSerializer(EducationServiceBaseSerializer):
    """Сериализация данных при получении одного объекта образовательных услуг (курсов)"""
    program = ProgramEducationServiceSerializer(
        label='ДПП'
    )


class EducationServiceAddUpdateSerializer(EducationServiceBaseSerializer):
    """Сериализация данных при получении одного объекта образовательных услуг (курсов)"""
    object_id = serializers.UUIDField(
        allow_null=True,
        label='object_id образовательной услуги (при обновлении)'
    )
    program = serializers.UUIDField(
        allow_null=False,
        label='object_id ДПП'
    )
