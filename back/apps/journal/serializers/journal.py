from rest_framework import serializers

from apps.journal.selectors.journal import journal_model
from apps.journal.services.output import OutputService
from apps.journal.services.payload import PayloadService

pu = PayloadService()
ou = OutputService()


class JournalSerializer(serializers.ModelSerializer):
    """Сериализация записей журнала событий"""
    date_create = serializers.DateTimeField(
        format='%d.%m.%Y %H:%M',
        label='Дата создания'
    )
    payload = serializers.SerializerMethodField(label='Полезная нагрузка')
    output = serializers.SerializerMethodField(label='Выходные данные')

    def get_payload(self, obj):
        payload = pu.get_payload(obj.object_id)
        if payload == '[]':
            return None
        return pu.get_payload(obj.object_id)

    def get_output(self, obj):
        return ou.get_output(obj.object_id)

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
