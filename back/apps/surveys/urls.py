from apps.surveys.routers.survey import survey_router
from apps.surveys.routers.survey_question import survey_question_router
from apps.surveys.routers.survey_question_answer import survey_question_answer_router
from apps.surveys.routers.survey_target import survey_target_urlpatterns

urlpatterns = (survey_router.urls +
               survey_question_router.urls +
               survey_question_answer_router.urls +
               survey_target_urlpatterns)
