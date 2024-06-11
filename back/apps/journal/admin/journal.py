from django.contrib import admin

from apps.journal.models import Journal
from apps.journal.services.output import OutputService
from apps.journal.services.payload import PayloadService


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    """Класс для отображения записей журнала событий в административной панели"""
    list_display = ('date_create', 'source', 'module', 'status', 'description', 'payload', 'output')
    list_filter = ('status', )
    search_fields = ('source', 'description')
    ordering = ('-date_create',)

    def payload(self, obj):
        """Получение полезной нагрузки"""
        pl = PayloadService().get_payload(obj.object_id)
        if pl is None:
            return '-'
        return pl

    def output(self, obj):
        """Получение результата/выходных данных"""
        pl = OutputService().get_output(obj.object_id)
        if pl is None:
            return '-'
        return pl

    payload.short_description = 'Полезная нагрузка'
    output.short_description = 'Выходные данные'
