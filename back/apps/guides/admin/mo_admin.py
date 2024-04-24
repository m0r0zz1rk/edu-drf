from django.contrib import admin

from apps.guides.models import Mo


@admin.register(Mo)
class MoAdmin(admin.ModelAdmin):
    """Класс для отображения муниципальных образований в административной панели"""

    list_display = ('name',)
    search_fields = ('name',)
