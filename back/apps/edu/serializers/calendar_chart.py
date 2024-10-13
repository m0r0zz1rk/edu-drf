from rest_framework import serializers

from apps.edu.selectors.calender_chart.calendar_chart_theme import calendar_chart_theme_model


class CalendarChartElementSerializer(serializers.ModelSerializer):
    """Сериализация данных для элементов КУГ"""
    object_id = serializers.UUIDField(
        allow_null=False,
        label='ID'
    )

    class Meta:
        model = calendar_chart_theme_model
        exclude = ('date_create', 'chapter')


class CalendarChartThemeSerializer(serializers.ModelSerializer):
    """Серилизация данных для тем разделов КУГ"""
    object_id = serializers.UUIDField(
        allow_null=False,
        label='ID'
    )
    chapter = serializers.UUIDField(
        allow_null=False,
        label='Object_id раздела'
    )

    class Meta:
        model = calendar_chart_theme_model
        exclude = ('date_create', )


class CalendarChartChapterSerializer(CalendarChartElementSerializer):
    """Сериализация данных для разделов КУГ"""
    themes = CalendarChartThemeSerializer(
        many=True,
        label='Темы'
    )
    program = serializers.UUIDField(
        allow_null=False,
        label='ДПП'
    )


class CalendarChartGetSerializer(serializers.Serializer):
    """Сериализация данных для получения КУГ"""
    on_edit = serializers.CharField(
        max_length=300,
        allow_null=True,
        allow_blank=True,
        label='КУГ на редактировании'
    )
    chapters = CalendarChartChapterSerializer(
        many=True,
        label='Разделы'
    )


class CalendarChartUpdateSerializer(serializers.Serializer):
    """Сериализация данных для обновленияКУГ"""
    program_id = serializers.UUIDField(
        allow_null=False,
        label='Object_id ДПП'
    )
    chapters = CalendarChartChapterSerializer(
        many=True,
        label='Разделы'
    )


class CalendarChartThemeRemainHoursSerializer(serializers.Serializer):
    """Сериализация объекта с информацией по оставшимся для расписания часам темы КУГ"""
    theme = serializers.CharField(
        max_length=500,
        allow_null=False,
        allow_blank=False,
        label='Тема'
    )
    theme_id = serializers.UUIDField(
        allow_null=False,
        label='object_id темы'
    )
    lecture = serializers.IntegerField(
        min_value=0,
        label='Лекционные часы'
    )
    practice = serializers.IntegerField(
        min_value=0,
        label='Часы практики'
    )
    trainee = serializers.IntegerField(
        min_value=0,
        label='Часы стажировки'
    )
    individual = serializers.IntegerField(
        min_value=0,
        label='Часы самостоятельной работы'
    )


class CalendarChartChapterRemainHoursSerializer(serializers.Serializer):
    """Сериализация объекта с информацией об остаточных часах раздела КУГ"""
    chapter = serializers.CharField(
        max_length=500,
        allow_blank=False,
        allow_null=False,
        label='Наименование раздела КУГ'
    )
    themes = CalendarChartThemeRemainHoursSerializer(
        many=True,
        label='Информация об остаточных часах тем раздела'
    )


class CalendarChartRemainHoursSerializer(serializers.Serializer):
    """Сериализация списка оставшихся для расписания часов КУГ"""
    kug_remain = CalendarChartChapterRemainHoursSerializer(
        many=True,
        label='Информация об остаточных часах разделов КУГ'
    )
