from django.contrib import admin

from apps.guides.models import EventType


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    """Класс для отображения типов мероприятий в административной панели"""

    list_display = ('name',)
    search_fields = ('name',)
