from django.contrib import admin

from apps.surveys.selectors.survey_question_answer import survey_question_answer_model


@admin.register(survey_question_answer_model)
class SurveyQuestionAnswerAdmin(admin.ModelAdmin):
    """Класс отображения заготовленных ответов к вопросам опросов в административной панели"""

    list_display = (
        'survey_question',
        'text'
    )

    search_fields = (
        'survey_question__text',
    )
