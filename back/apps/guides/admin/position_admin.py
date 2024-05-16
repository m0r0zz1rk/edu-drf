
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.guides.models import Position


class PositionResource(resources.ModelResource):
    """Класс описания ресурса для импорта/экспорта данных в Excel из административной панели"""
    class Meta:
        model = Position
        exclude = ('date_create', )
        import_id_fields = ['object_id', ]


@admin.register(Position)
class PositionAdmin(ImportExportModelAdmin):
    """Класс для отображения должностей в административной панели"""
    resource_class = PositionResource
    sortable_by = ('name',)
    list_display = ('name',)
    search_fields = ('name',)
