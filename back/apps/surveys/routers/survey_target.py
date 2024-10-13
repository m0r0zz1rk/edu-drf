from apps.commons.drf.routers.list_create_update_delete_router import ListCreateUpdateDeleteRouter
from apps.surveys.api.survey_target import SurveyTargetViewSet

survey_target_router = ListCreateUpdateDeleteRouter(trailing_slash=True)
survey_target_router.register('survey_target', SurveyTargetViewSet)

survey_target_urlpatterns = [

]

survey_target_urlpatterns += survey_target_router.urls
