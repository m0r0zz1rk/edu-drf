from rest_framework import serializers

from apps.edu.selectors.planning_parameter import planning_parameter_model


class PlanningParameterSerializer(serializers.ModelSerializer):
    """Сериализация данных для параметров планирования мероприятий"""
    object_id = serializers.UUIDField(
        allow_null=False,
        label='object_id параметра'
    )

    class Meta:
        model = planning_parameter_model
        exclude = ('date_create', 'old_id', 'name')
