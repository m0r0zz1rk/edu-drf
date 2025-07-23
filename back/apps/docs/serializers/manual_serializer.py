import base64

from rest_framework import serializers


class ManualSerializer(serializers.Serializer):
    """Сериализация данных при получении руководства пользователя"""

    file = serializers.SerializerMethodField(
        label='Файл в формате base64'
    )

    def get_file(self, obj):
        try:
            with open(obj.get('file'), mode='rb') as doc_file:
                doc_data = doc_file.read()
            return base64.b64encode(doc_data).decode('utf-8')
        except Exception as e:
            return None
