from django.contrib import admin

from apps.journal.models import JournalOutput


@admin.register(JournalOutput)
class OutputAdmin(admin.ModelAdmin):
    """Класс для отображения выходных данных к записям журнала событий"""
    list_display = ('journal_rec', 'output')
    search_fields = ('journal_rec__object_id', 'output')
