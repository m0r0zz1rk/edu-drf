from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.guides.selectors.region import region_model


class RegionResource(resources.ModelResource):
    """Класс описания ресурса для импорта/экспорта регионов РФ в Excel из административной панели"""
    class Meta:
        model = region_model
        exclude = ('date_create', )
        import_id_fields = ['object_id', ]


@admin.register(region_model)
class RegionAdmin(ImportExportModelAdmin):
    """Класс для отображения модели регионов РФ в административной панели"""
    resource_class = RegionResource
    sortable_by = ('name', )
    list_display = ('name', )
    search_fields = ('name', )
