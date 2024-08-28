from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from apps.guides.models import Oo
from apps.guides.selectors.mo import mo_model
from apps.guides.selectors.oo_type import oo_type_model


class OoResources(resources.ModelResource):
    """Класс описания ресурса для загрузки/выгрузки в Excel"""
    mo = Field(
        attribute="mo",
        widget=ForeignKeyWidget(mo_model, "name")
    )
    oo_type = Field(
        attribute="oo_type",
        widget=ForeignKeyWidget(oo_type_model, "name")
    )

    class Meta:
        model = Oo
        import_id_fields = ['object_id', ]
        exclude = ['date_create', ]


@admin.register(Oo)
class OoAdmin(ImportExportModelAdmin):
    """Класс для отображения образовательных организаций в административной панели"""
    resource_class = OoResources
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
