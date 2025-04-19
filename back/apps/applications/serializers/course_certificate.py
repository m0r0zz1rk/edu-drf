from rest_framework import serializers

from apps.applications.selectors.course_certificate import course_certificate_model


class BaseCertificateSerializer(serializers.ModelSerializer):
    """Базовая сериализация данных модели удостоверений"""
    class Meta:
        model = course_certificate_model
        fields = (
            'registration_number',
            'blank_serial',
            'blank_number'
        )


class CourseCertificateUpdateSerializer(BaseCertificateSerializer):
    class Meta(BaseCertificateSerializer.Meta):
        model = course_certificate_model
        fields = BaseCertificateSerializer.Meta.fields + ('object_id', )


class CourseCertificateListSerializer(CourseCertificateUpdateSerializer):
    """
    Сериализация данных при получении списка с информацией об удостоврениям к заявкам на курс
    """
    student = serializers.SerializerMethodField(
        label='ФИО обучающегося'
    )

    def get_student(self, obj):
        profile = obj.application.profile
        display_name = f'{profile.surname} {profile.name}'
        if profile.patronymic:
            display_name += f' {profile.patronymic}'
        return {
            'display_name': display_name,
            'email': profile.django_user.email,
            'phone': profile.phone
        }

    class Meta(CourseCertificateUpdateSerializer.Meta):
        fields = CourseCertificateUpdateSerializer.Meta.fields + ('student', )


class CourseCertificateGenerateSerializer(serializers.Serializer):
    """Сериализация данных при генереации информации об удостоверениях"""
    registration_number = serializers.CharField(
        max_length=50,
        allow_null=False,
        allow_blank=False,
        label='Подрядковый регистрационный номер'
    )
    blank_serial = serializers.CharField(
        max_length=50,
        allow_null=False,
        allow_blank=False,
        label='Серия бланка удостоверения'
    )
    blank_number = serializers.CharField(
        max_length=50,
        allow_null=False,
        allow_blank=False,
        label='Номер бланка удостоверения'
    )
    group_id = serializers.UUIDField(
        allow_null=False,
        label='object_id учебной группы'
    )
