from django.contrib import admin

from apps.guides.models import AudienceCategory


@admin.register(AudienceCategory)
class AudienceCategoryAdmin(admin.ModelAdmin):
    """Класс для отображения категорий слушателей в административной панели"""

    list_display = ('name', )
    search_fields = ('name', )
