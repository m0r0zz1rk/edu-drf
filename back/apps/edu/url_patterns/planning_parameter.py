from django.urls import path

from apps.edu.api.planning_parameter import PlanningParameterViewSet

planning_parameter_urlpatterns = [
    path('planning_parameter/', PlanningParameterViewSet.as_view({'get': 'list'})),
    path('planning_parameter/update/', PlanningParameterViewSet.as_view({'patch': 'update'})),
]
