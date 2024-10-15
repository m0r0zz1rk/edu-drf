import base64

from rest_framework import serializers


class DocViewerSerializer(serializers.Serializer):
    """
    Сериализация файла для просмотран на web форме
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
            with obj['file'].open(mode='rb') as doc_file:
                doc_data = doc_file.read()
            return base64.b64encode(doc_data).decode('utf-8')
        except Exception:
            return None
