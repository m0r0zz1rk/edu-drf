from django.apps import apps
from rest_framework import serializers

from apps.journal.utils.output_utils import OutputUtils
from apps.journal.utils.payload_utils import PayloadUtils

journal_model = apps.get_model('journal', 'Journal')

pu = PayloadUtils()
ou = OutputUtils()


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
