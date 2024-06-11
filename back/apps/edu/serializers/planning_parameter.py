from django.apps import apps
from rest_framework import serializers

planning_parameter_model = apps.get_model('edu', 'PlanningParameter')


class PlanningParameterSerializer(serializers.ModelSerializer):
    """Сериализация данных для параметров планирования мероприятий"""
    object_id = serializers.UUIDField(
        allow_null=False,
        label='object_id параметра'
    )

    class Meta:
        model = planning_parameter_model
        exclude = ('date_create', 'name')
