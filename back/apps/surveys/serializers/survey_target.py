from rest_framework import serializers

from apps.surveys.consts.survey_target_types import SURVEY_TARGET_TYPES
from apps.surveys.selectors.survey_target import survey_target_model


class SurveyTargetCreateSerializer(serializers.ModelSerializer):
    """Сериализация данных при добавлении назначения опроса"""

    survey_id = serializers.UUIDField(
        allow_null=False,
        label='object_id опроса'
    )
    group_id = serializers.UUIDField(
        allow_null=True,
        label='Учебная группа'
    )

    class Meta:
        model = survey_target_model
        fields = (
            'object_id',
            'survey_id',
            'type',
            'group_id'
        )


class SurveyTargetListSerializer(serializers.ModelSerializer):
    """Сериализация данных при получении списка таргетирований опросов"""

    survey_description = serializers.SerializerMethodField(
        label='Описание опроса'
    )
    type = serializers.SerializerMethodField(
        label='Тип таргетирования'
    )
    group_id = serializers.UUIDField(
        allow_null=True,
        label='Учебная группа'
    )
    group_code = serializers.SerializerMethodField(
        label='Код учебной группы'
    )

    def get_type(self, obj):
        for type in SURVEY_TARGET_TYPES:
            if type[0] == obj.type:
                return type[1]

    def get_survey_description(self, obj):
        return obj.survey.description

    def get_group_code(self, obj):
        if obj.group:
            return obj.group.code
        return None

    class Meta:
        model = survey_target_model
        fields = (
            'object_id',
            'survey_id',
            'survey_description',
            'type',
            'group_id',
            'group_code'
        )
