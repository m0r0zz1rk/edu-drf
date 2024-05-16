from django.contrib import admin

from apps.commons.models.ad_centre import AdCentre
from apps.commons.models.ad_centre_coko_user import AdCentreCokoUser


@admin.register(AdCentre)
class AdCentreAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'object_guid')
    search_fields = ('display_name', 'object_guid')


@admin.register(AdCentreCokoUser)
class AdCentreCokoUserAdmin(admin.ModelAdmin):
    pass
