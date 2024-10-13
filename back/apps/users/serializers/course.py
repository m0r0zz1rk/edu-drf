from rest_framework import serializers

from apps.authen.services.profile import ProfileService
from apps.edu.selectors.student_group import student_group_model

profile_service = ProfileService()


class CoursesDepartmentSerializer(serializers.ModelSerializer):
    """
    Сериализация данных при получении списка доступных курсов
    для структурного подразделения
    """

    course_title = serializers.SerializerMethodField(
        label='Наименование услуги'
    )
    date_start = serializers.SerializerMethodField(
        label='Дата начала обучения'
    )
    date_end = serializers.SerializerMethodField(
        label='Дата окончания обучения'
    )
    service_type = serializers.SerializerMethodField(
        label='Тип ДПП'
    )
    program_duration = serializers.SerializerMethodField(
        label='Объем программы (часов)'
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

    def get_course_title(self, obj):
        if obj.ou:
            if obj.ou.program:
                return obj.ou.program.name
        return '-'

    def get_date_start(self, obj):
        if obj.ou:
            return obj.ou.date_start.strftime('%d.%m.%Y')
        return '-'

    def get_date_end(self, obj):
        if obj.ou:
            return obj.ou.date_end.strftime('%d.%m.%Y')
        return '-'

    def get_service_type(self, obj):
        if obj.ou:
            if obj.ou.program:
                return obj.ou.program.type
        return '-'

    def get_program_duration(self, obj):
        if obj.ou:
            if obj.ou.program:
                return obj.ou.program.duration
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
            'course_title',
            'code',
            'date_start',
            'date_end',
            'service_type',
            'program_duration',
            'curator_fio',
            'curator_email',
            'curator_phone'
        )


class CoursesListSerializer(serializers.Serializer):
    """Сериализация данных при получении списка курсов для регистрации"""
    department = serializers.CharField(
        max_length=300,
        allow_null=False,
        allow_blank=False,
        label='Подразделение ЦОКО'
    )
    courses = CoursesDepartmentSerializer(
        many=True,
        label='Курсы подразделения'
    )
