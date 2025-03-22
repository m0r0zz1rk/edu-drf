from rest_framework import serializers

from apps.journal.selectors.journal import journal_model
from apps.journal.services.output import output_service
from apps.journal.services.payload import payload_service


class JournalSerializer(serializers.ModelSerializer):
    """Сериализация записей журнала событий"""
    date_create = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        label='Дата создания'
    )
    payload = serializers.SerializerMethodField(label='Полезная нагрузка')
    output = serializers.SerializerMethodField(label='Выходные данные')

    def get_payload(self, obj):
        payload = payload_service.get_payload(obj.object_id)
        return None if payload == '[]' else payload

    def get_output(self, obj):
        return output_service.get_output(obj.object_id)

    class Meta:
        model = journal_model
        fields = [
            'date_create',
            'source',
            'module',
            'status',
            'description',
            'payload',
            'output'
        ]
