from django.urls import path

from apps.guides.api.state_viewset import StateViewSet

state_urlpatterns = [
    path('states/', StateViewSet.as_view({'get': 'list'}))
]

urlpatterns = state_urlpatterns
