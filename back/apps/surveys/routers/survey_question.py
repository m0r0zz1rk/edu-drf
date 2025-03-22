from apps.commons.drf.routers.LCUD_router import ListCreateUpdateDeleteRouter
from apps.surveys.api.survey_question import SurveyQuestionViewSet

survey_question_router = ListCreateUpdateDeleteRouter(trailing_slash=True)
survey_question_router.register('survey_questions', SurveyQuestionViewSet)
