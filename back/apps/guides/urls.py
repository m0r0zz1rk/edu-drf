from django.urls import path

from apps.guides.api.state_viewset import StateViewSet
from apps.guides.api.user_viewset import UserViewSet

state_urlpatterns = [
    path('states/', StateViewSet.as_view({'get': 'list'}))
]

user_urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list'})),
]

urlpatterns = state_urlpatterns + user_urlpatterns

