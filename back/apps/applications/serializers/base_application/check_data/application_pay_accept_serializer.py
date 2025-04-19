from rest_framework import serializers

from apps.applications.selectors.course_application import course_application_model


class ApplicationPayAcceptSerializer(serializers.ModelSerializer):
    """
    Сериализация при подтвержденной оплате
    """
    class Meta:
        model = course_application_model
        fields = ('status', )
