import base64
import os.path

from rest_framework import serializers

from apps.commons.utils.data_types.file import file_utils
from apps.commons.utils.django.exception import ExceptionHandling

# Форматы изображений
img_formats = ['.jpg', '.jpeg', '.png']

class DocViewerSerializer(serializers.Serializer):
    """
    Сериализация файла для просмотра на web форме
    """

    file_name = serializers.CharField(
        max_length=1000,
        allow_null=False,
        allow_blank=False,
        label='Имя файла'
    )
    file = serializers.SerializerMethodField(
        label='Файл в формате base64'
    )

    def get_file(self, obj):
        try:
            _, extension = os.path.splitext(obj.get('file').path)
            if extension.lower() in img_formats:
                doc_data = file_utils.jpg_to_pdf(obj.get('file').path)
            else:
                with obj['file'].open(mode='rb') as doc_file:
                    doc_data = doc_file.read()
            print('doc_data: ', doc_data)
            return base64.b64encode(doc_data).decode('utf-8')
        except Exception as e:
            print('Exception: ', ExceptionHandling.get_traceback())
            return str(e)
