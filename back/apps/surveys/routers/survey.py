from apps.commons.drf.routers.LCU_router import ListCreateUpdateRouter
from apps.surveys.api.survey import SurveyViewSet

survey_router = ListCreateUpdateRouter(trailing_slash=True)
survey_router.register('surveys', SurveyViewSet)
