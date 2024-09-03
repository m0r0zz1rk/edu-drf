from rest_framework import serializers

from apps.authen.services.profile import ProfileService
from apps.commons.utils.data_types.date import DateUtils
from apps.edu.selectors.schedule import schedule_model

profile_service = ProfileService()
date_utils = DateUtils()


class LessonSerializer(serializers.ModelSerializer):
    """Сериализация данных для одного занятия учебной группы"""
    teacher_fio = serializers.SerializerMethodField()
    time_start_str = serializers.SerializerMethodField()
    time_end_str = serializers.SerializerMethodField()

    def get_teacher_fio(self, obj):
        """Получение ФИО преподавателя занятия"""
        if obj['teacher']:
            return profile_service.get_profile_or_info_by_attribute(
                'object_id',
                obj.teacher,
                'display_name'
            )
        return '-'

    def get_time_start_str(self, obj):
        """Преобразование количества секунд времени начала занятия в формат ЧЧ:ММ"""
        return date_utils.convert_seconds_to_time_string(obj['time_start'])

    def get_time_end_str(self, obj):
        """Преобразование количества секунд времени окончания занятия в формат ЧЧ:ММ"""
        return date_utils.convert_seconds_to_time_string(obj['time_end'])

    class Meta:
        model = schedule_model
        fields = (
            'time_start_str',
            'time_end_str',
            'theme',
            'lecture_hours',
            'practice_hours',
            'trainee_hours',
            'individual_hours',
            'teacher_fio',
            'distance',
            'control'
        )


class ScheduleListSerializer(serializers.Serializer):
    """Сериализация данных при получении расписания занятий учебной группы"""
    day = serializers.RegexField(
        '[0-9]{2}.[0-9]{2}.[0-9]{4}',
        label='Учебный день'
    )
    lessons = LessonSerializer(
        many=True,
        label='Занятия'
    )


class GenerateDaySerializer(serializers.Serializer):
    """Сериализация параметров учебного дня для генерации занятий учебной группы"""
    day = serializers.RegexField(
        "[0-9]{2}.[0-9]{2}.[0-9]{4}",
        label='Учебный день'
    )
    study_day = serializers.BooleanField(
        label='Наличие занятий'
    )
    time_start = serializers.RegexField(
        "[0-9]{2}:[0-9]{2}",
        label='Время начала первого занятия'
    )
    hours_count = serializers.IntegerField(
        max_value=6,
        min_value=1,
        label='Количество академических часов'
    )


class GenerateScheduleSerializer(serializers.Serializer):
    """Генерация списка параметров учебного дня для генерации расписания учебной группы"""
    group_id = serializers.UUIDField(
        allow_null=False,
        label='object_id учебной группы'
    )
    generate = GenerateDaySerializer(
        many=True,
        label='Параметры генерации'
    )
