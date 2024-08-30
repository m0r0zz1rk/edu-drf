from rest_framework import serializers

from apps.authen.services.profile import ProfileService
from apps.edu.selectors.schedule import schedule_model

profile_service = ProfileService()


class LessonSerializer(serializers.ModelSerializer):
    """Сериализация данных для одного занятия учебной группы"""
    teacher_fio = serializers.SerializerMethodField()

    def get_teacher_fio(self, obj):
        """Получение ФИО преподавателя занятия"""
        if obj.teacher:
            return profile_service.get_profile_or_info_by_attribute(
                'object_id',
                obj.teacher,
                'display_name'
            )
        return '-'

    class Meta:
        model = schedule_model
        fields = (
            'time_start',
            'time_end',
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
    day = serializers.CharField()
    lessons = LessonSerializer(many=True, read_only=True)
