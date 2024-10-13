from django.contrib import admin

from apps.surveys.selectors.student_answer import student_answer_model


@admin.register(student_answer_model)
class StudentAnswerAdmin(admin.ModelAdmin):
    """Класс отображения ответов обучающихся в административной панели"""

    list_display = (
        'survey',
        'question',
        'answer'
    )

    search_fields = (
        'survey__description',
        'question',
    )
