from django.contrib import admin

from apps.journal.models import Journal
from apps.journal.utils.output_utils import OutputUtils
from apps.journal.utils.payload_utils import PayloadUtils


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    """Класс для отображения записей журнала событий в административной панели"""
    list_display = ('source', 'module', 'status', 'description', 'payload', 'output')
    list_filter = ('status', )
    search_fields = ('source', 'description')

    def payload(self, obj):
        """Получение полезной нагрузки"""
        pl = PayloadUtils().get_payload(obj.object_id)
        if pl is None:
            return '-'
        return pl

    def output(self, obj):
        """Получение результата/выходных данных"""
        pl = OutputUtils().get_output(obj.object_id)
        if pl is None:
            return '-'
        return pl

    payload.short_description = 'Полезная нагрузка'
    output.short_description = 'Выходные данные'
