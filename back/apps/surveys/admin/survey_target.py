from django.contrib import admin

from apps.surveys.selectors.survey_target import survey_target_model


@admin.register(survey_target_model)
class SurveyTargetAdmin(admin.ModelAdmin):
    """Класс отображения назначений опросов в административной панели"""

    list_display = (
        'survey',
        'type'
    )

    search_fields = (
        'survey__description'
    )
