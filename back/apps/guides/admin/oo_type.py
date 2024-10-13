from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.guides.selectors.oo_type import oo_type_model


class OoTypeResource(resources.ModelResource):
    """Класс описания ресурса для импорта/экспорта типов ОО в Excel из административной панели"""
    class Meta:
        model = oo_type_model
        exclude = ('date_create', )
        import_id_fields = ['object_id', ]


@admin.register(oo_type_model)
class OoTypeAdmin(ImportExportModelAdmin):
    """Класс для отображения типов образовательных организаций в административной панели"""
    resource_class = OoTypeResource
    list_display = ('name',)
    search_fields = ('name',)
