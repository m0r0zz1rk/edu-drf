from rest_framework import serializers


class TeacherSerializer(serializers.Serializer):
    """Сериализация данных для преподавателя в расписание"""
    object_id = serializers.UUIDField(
        allow_null=False,
        label='object_id пользователя'
    )
    surname = serializers.CharField(
        max_length=150,
        label='Фамилия'
    )
    name = serializers.CharField(
        max_length=150,
        label='Имя'
    )
    patronymic = serializers.CharField(
        max_length=150,
        label='Отчество'
    )
    phone = serializers.CharField(
        max_length=18,
        allow_null=True,
        allow_blank=True,
        label='Номер телефона'
    )


class CheckTeacherBusySerializer(serializers.Serializer):
    """Сериализация данных при проверке занятости преподавателя для проведения занятия"""
    teacher_id = serializers.UUIDField(
        allow_null=False,
        label='object_id внешнего преподавателя или сотрудника ЦОКО'
    )
    group_id = serializers.UUIDField(
        allow_null=False,
        label='object_id учебной группы'
    )
    day = serializers.DateField(
        input_formats=['%d.%m.%Y'],
        label='Дата проведения занятия'
    )
    time_start_str = serializers.CharField(
        label='Время проведения занятия в формате ЧЧ:ММ'
    )
