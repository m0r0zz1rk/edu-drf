from django.contrib import admin

from apps.guides.models import PositionCategory


@admin.register(PositionCategory)
class PositionCategoryAdmin(admin.ModelAdmin):
    """Класс для отображения категорий должностей в административной панели"""

    list_display = ('name',)
    search_fields = ('name',)
