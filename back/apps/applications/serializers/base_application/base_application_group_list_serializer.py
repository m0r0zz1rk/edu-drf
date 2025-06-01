import os

from rest_framework import serializers

from apps.applications.selectors.event_application import event_application_model
from apps.edu.selectors.student_group import student_group_queryset


class BaseApplicationGroupListSerializer(serializers.ModelSerializer):
    """Сериализация данных при получении списка заявок для учебной группы"""
    group = serializers.SlugRelatedField(
        slug_field='code',
        queryset=student_group_queryset,
        label='Учебная группа'
    )
    student = serializers.SerializerMethodField(
        label='Информация об обучающемся'
    )
    date_create = serializers.DateTimeField(
        format='%d.%m.%Y',
        label='Дата подачи заявки'
    )
    pay_doc_name = serializers.SerializerMethodField(
        label='Имя файла документа об оплате'
    )

    def get_student(self, obj):
        return {
            'profile_id': obj.profile.object_id,
            'display_name': obj.profile.display_name,
            'email': obj.profile.django_user.email,
            'phone': obj.profile.phone,
        }

    def get_pay_doc_name(self, obj):
        if obj.pay_doc:
            return os.path.basename(obj.pay_doc.file.name)
        return ''

    class Meta:
        model = event_application_model
        fields = (
            'object_id',
            'group',
            'student',
            'date_create',
            'status',
            'oo',
            'oo_new',
            'check_survey',
            'pay_doc_id',
            'pay_doc_name'
        )
