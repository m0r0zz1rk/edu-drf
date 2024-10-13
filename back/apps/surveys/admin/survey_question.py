from django.contrib import admin

from apps.surveys.selectors.survey_question import survey_question_model


@admin.register(survey_question_model)
class SurveyQuestionAdmin(admin.ModelAdmin):
    """Класс отображения вопросов опросов в административной панели"""
    list_display = (
        'survey',
        'sequence_number',
        'text'
    )

    search_fields = (
        'survey__description',
        'text'
    )
