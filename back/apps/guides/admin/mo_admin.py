from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.guides.models import Mo


class MoResource(resources.ModelResource):
    """Класс описания ресурса для импорта/экспорта данных в Excel из административной панели"""
    class Meta:
        model = Mo
        fields = ['object_id', 'name']
        import_id_fields = ['object_id', ]


@admin.register(Mo)
class MoAdmin(ImportExportModelAdmin):
    """Класс для отображения муниципальных образований в административной панели"""
    resource_class = MoResource
    list_display = ('name',)
    search_fields = ('name',)
