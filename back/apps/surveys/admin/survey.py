from django.contrib import admin

from apps.authen.services.profile import ProfileService
from apps.surveys.selectors.survey import survey_model


@admin.register(survey_model)
class SurveyAdmin(admin.ModelAdmin):
    """Класс для вывода опросов в административную панель"""
    list_display = (
        'object_id',
        'creator_fio',
        'description'
    )

    search_fields = ('description', )

    _profile_service = ProfileService()

    def creator_fio(self, obj):
        """Получение ФИО создателя опроса"""
        if obj.creator:
            return self._profile_service.get_profile_or_info_by_attribute(
                'django_user_id',
                obj.creator_id,
                'display_name'
            )
        return '-'

    creator_fio.short_description = 'Создатель'
