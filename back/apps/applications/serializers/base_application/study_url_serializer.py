from rest_framework import serializers


class StudyUrlSerializer(serializers.Serializer):
    """Сериализация ссылка на обучение в учебной группе"""
    study_url = serializers.URLField(
        max_length=3000,
        allow_null=True,
        label='Ссылка на обучение'
    )
