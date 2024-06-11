from django.contrib import admin

from apps.journal.models import JournalPayload


@admin.register(JournalPayload)
class PayloadAdmin(admin.ModelAdmin):
    """Класс для отображения полезной нагрузки к записям журнала событий"""
    list_display = ('journal_rec', 'payload')
    search_fields = ('journal_rec__object_id', 'payload')
