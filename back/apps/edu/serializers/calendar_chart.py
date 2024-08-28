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
