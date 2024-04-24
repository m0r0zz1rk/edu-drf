from django.contrib import admin

from apps.guides.models import Oo


@admin.register(Oo)
class OoAdmin(admin.ModelAdmin):
    """Класс для отображения образовательных организаций в административной панели"""

    list_display = ('mo_name', 'short_name', 'full_name', 'oo_type_name', 'form')
    list_filter = ('mo', 'oo_type')
    search_fields = ('short_name', 'full_name', 'form')

    def mo_name(self, obj):
        """Отображение наименования муниципального образования"""
        if obj.mo is not None:
            return obj.mo.name
        return '-'

    def oo_type_name(self, obj):
        """Отображение типа образовательной организации"""
        if obj.oo_type is not None:
            return obj.oo_type.name
        return '-'

    mo_name.short_description = 'МО'
    oo_type_name.short_description = 'Тип'
