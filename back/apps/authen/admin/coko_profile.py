from django.contrib import admin

from apps.authen.models.coko_profile import CokoProfile


@admin.register(CokoProfile)
class CokoProfileAdmin(admin.ModelAdmin):
    """Класс для отображения профилей сотрудников ЦОКО в административной панели"""

    list_display = (
        'surname',
        'name',
        'patronymic',
    )
    search_fields = (
        'surname',
        'name',
        'patronymic',
    )
