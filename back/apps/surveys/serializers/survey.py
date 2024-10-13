from rest_framework import serializers

from apps.authen.services.profile import ProfileService
from apps.surveys.exceptions.survey import SurveyNotExist
from apps.surveys.selectors.survey import survey_model
from apps.surveys.services.survey_question import SurveyQuestionService

profile_service = ProfileService()


class SurveyBaseSerializer(serializers.ModelSerializer):
    """Сериализация базовых полей модели опросов"""
    class Meta:
        model = survey_model
        fields = (
            'description',
        )


class SurveyCreateSerializer(SurveyBaseSerializer):
    """Сериализация данных при добавлении нового опроса"""
    class Meta(SurveyBaseSerializer.Meta):
        fields = SurveyBaseSerializer.Meta.fields + (
            'object_id',
        )


class SurveyListSerializer(SurveyCreateSerializer):
    """Сериализация данных при получении списка опросов"""
    creator_fio = serializers.SerializerMethodField(
        label='ФИО создателя запроса'
    )
    question_count = serializers.SerializerMethodField(
        label='Количество вопросов опроса'
    )

    def get_creator_fio(self, obj):
        """Получение ФИО создателя опроса"""
        if obj.creator:
            return profile_service.get_profile_or_info_by_attribute(
                'django_user_id',
                obj.creator_id,
                'display_name'
            )
        return '-'

    def get_question_count(self, obj):
        """Получение количества вопросов опроса"""
        try:
            return SurveyQuestionService(obj.object_id).get_question_count()
        except SurveyNotExist:
            return '-'

    class Meta(SurveyCreateSerializer.Meta):
        fields = SurveyCreateSerializer.Meta.fields + (
            'creator_fio',
            'question_count'
        )
