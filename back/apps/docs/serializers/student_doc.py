import base64
import os

from rest_framework import serializers

from apps.commons.drf.base64_coko_file_field import Base64CokoFileField
from apps.docs.consts.student_doc_types import STUDENT_DOC_TYPES
from apps.docs.selectors.student_doc import student_doc_model


class StudentDocListSerializer(serializers.ModelSerializer):
    """Сериализация данных при получении списка документов пользователя"""

    date_create = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        label='Дата добавления документа'
    )
    doc_type = serializers.SerializerMethodField(
        label='Тип документа'
    )
    doc_name = serializers.SerializerMethodField(
        label='Имя документа'
    )
    file = serializers.SerializerMethodField(
        label='Файл документа'
    )

    def get_doc_name(self, obj):
        return os.path.basename(obj.file.name)

    def get_file(self, obj):
        try:
            with obj.file.open(mode='rb') as doc_file:
                doc_data = doc_file.read()
            return base64.b64encode(doc_data).decode('utf-8')
        except Exception:
            return None

    def get_doc_type(self, obj):
        for doc_type in STUDENT_DOC_TYPES:
            if doc_type[0] == obj.doc_type:
                return doc_type[1]
        return obj.doc_type

    class Meta:
        model = student_doc_model
        fields = (
            'object_id',
            'date_create',
            'doc_type',
            'doc_name'
        )


class StudentDocCreateSerializer(serializers.ModelSerializer):
    """Сериализация данных при добавлении нового документа обучающегося"""
    doc_type = serializers.CharField(
        max_length=50,
        allow_null=False,
        allow_blank=False,
        label='Тип документа'
    )
    file = Base64CokoFileField(
        required=True,
        allow_null=False
    )

    class Meta:
        model = student_doc_model
        fields = ('doc_type', 'file')
