from django.urls import path

from apps.surveys.api.survey_report import SurveyReportViewSet
from apps.surveys.routers.survey import survey_router
from apps.surveys.routers.survey_question import survey_question_router
from apps.surveys.routers.survey_question_answer import survey_question_answer_router
from apps.surveys.routers.survey_target import survey_target_urlpatterns

urlpatterns = [
    path('generate_report/', SurveyReportViewSet.as_view({'post': 'generate_report'}))
]

urlpatterns += (survey_router.urls +
                survey_question_router.urls +
                survey_question_answer_router.urls +
                survey_target_urlpatterns)
