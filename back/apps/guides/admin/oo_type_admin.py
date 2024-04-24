from django.contrib import admin

from apps.guides.models import OoType


@admin.register(OoType)
class OoTypeAdmin(admin.ModelAdmin):
    """Класс для отображения типов образовательных организаций в административной панели"""

    list_display = ('name',)
    search_fields = ('name',)
