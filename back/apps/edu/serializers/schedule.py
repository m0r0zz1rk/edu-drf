from rest_framework import serializers

from apps.edu.selectors.schedule import schedule_model


class ScheduleListSerializer(serializers.ModelSerializer):
    """Сериализация данных при получении расписания занятий учебной группы"""
    class Meta:
        model = schedule_model
        exclude = ('date_create', )
