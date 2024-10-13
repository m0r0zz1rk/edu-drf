from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.guides.selectors.position_category import position_category_model


class PositionCategoryResource(resources.ModelResource):
    """Класс описания ресурса для импорта/экспорта категорий должностей в Excel из административной панели"""
    class Meta:
        model = position_category_model
        exclude = ('date_create', )
        import_id_fields = ['object_id', ]


@admin.register(position_category_model)
class PositionCategoryAdmin(ImportExportModelAdmin):
    """Класс для отображения категорий должностей в административной панели"""
    resource_class = PositionCategoryResource
    list_display = ('name',)
    search_fields = ('name',)
