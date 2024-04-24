from django.contrib import admin

from apps.guides.models import Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Класс для отображения должностей в административной панели"""

    list_display = ('name',)
    search_fields = ('name',)
