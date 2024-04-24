from django.contrib import admin

from apps.guides.models import State


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    """Класс для отображения государств в административной панели"""

    list_display = ('name',)
    search_fields = ('name',)
