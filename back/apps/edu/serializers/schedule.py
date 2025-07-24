from rest_framework import serializers

from apps.authen.services.profile import profile_service
from apps.commons.utils.data_types.date import DateUtils
from apps.edu.selectors.schedule import schedule_model

date_utils = DateUtils()


class LessonSerializer(serializers.ModelSerializer):
    """Сериализация данных для одного занятия учебной группы"""
    teacher = serializers.UUIDField(
        allow_null=True,
        label='uuid преподавателя (при наличии)'
    )
    teacher_fio = serializers.SerializerMethodField(
        label='ФИО преподавателя (при наличии)'
    )
    time_start_str = serializers.SerializerMethodField(
        label='Строковое представление ЧЧ:ММ начала занятия'
    )
    time_end_str = serializers.SerializerMethodField(
        label='Строковое представление ЧЧ:ММ окончания занятия'
    )

    def get_teacher_fio(self, obj):
        """Получение ФИО преподавателя занятия"""
        if obj['teacher']:
            return profile_service.get_profile_or_info_by_attribute(
                'object_id',
                obj['teacher'],
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
            'kug_theme_id',
            'theme',
            'type',
            'teacher',
            'teacher_fio',
            'distance',
            'control'
        )


class ScheduleListSerializer(serializers.Serializer):
    """Сериализация данных при получении расписания занятий учебной группы"""
    day = serializers.DateField(
        input_formats=['%d.%m.%Y'],
        label='Учебный день'
    )
    lessons = LessonSerializer(
        many=True,
        label='Занятия'
    )


class LessonInfoSerializer(serializers.Serializer):
    """Сериализация данных одного занятия при сохранении информации об учебном дне"""
    time_start_str = serializers.RegexField(
        '[0-2][0-9]:[0-5][0-9]',
        label='Время начала занятия'
    )
    time_end_str = serializers.RegexField(
        '[0-2][0-9]:[0-5][0-9]',
        label='Время окончания занятия'
    )
    kug_theme_id = serializers.UUIDField(
        allow_null=True,
        label='object_id темы раздела КУГ'
    )
    theme = serializers.CharField(
        max_length=500,
        label='Тема'
    )
    type = serializers.CharField(
        max_length=25,
        label='Тип занятия'
    )
    teacher = serializers.UUIDField(
        allow_null=True,
        label='object_id профиля сотрудника ЦОКО или внешнего пользователя преподавателя'
    )
    distance = serializers.BooleanField(
        label='Дистанционное занятие'
    )
    control = serializers.CharField(
        max_length=150,
        allow_null=True,
        allow_blank=True,
        label='Форма контроля'
    )


class DayInfoSerializer(serializers.Serializer):
    """Сериализация данных при сохранения расписания учебного дня"""
    group_id = serializers.UUIDField(
        allow_null=False,
        label='object_id учбеной группы'
    )
    day = serializers.DateField(
        input_formats=['%d.%m.%Y'],
        label='Учебный день'
    )
    lessons = LessonInfoSerializer(
        many=True,
        label='Информация по занятиям'
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
        max_value=9,
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


class PersonalDayScheduleSerializer(serializers.Serializer):
    """Сериализация данных при получении личного расписания преподавателя за один день"""

    group_code = serializers.CharField(
        max_length=50,
        label='Шифр учебной группы'
    )
    time_start_str = serializers.CharField(
        max_length=5,
        label='Время начала занятия'
    )
    time_end_str = serializers.CharField(
        max_length=5,
        label='Время окончания занятия'
    )
    lesson_theme = serializers.CharField(
        max_length=1000,
        label='Тема занятия'
    )
    type = serializers.CharField(
        max_length=15,
        label='Тип занятия'
    )
    distance = serializers.BooleanField(
        label='Дистант'
    )
    control = serializers.CharField(
        max_length=150,
        allow_null=True,
        label='Форма контроля'
    )


class PersonalScheduleSerializer(serializers.Serializer):
    """Сериализация данных при получении личного расписания преподавателя"""
    date = serializers.DateField(
        format=['%d.%m.%Y',],
        label='Дата занятий'
    )
    lessons = PersonalDayScheduleSerializer(
        many=True,
        label='Занятия'
    )
