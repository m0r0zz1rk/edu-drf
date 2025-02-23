from django.urls import path

from apps.guides.api.state.state_registration import StateRegistrationViewSet

state_registration_urlpatterns = [
    path('states/', StateRegistrationViewSet.as_view({'get': 'list'}))
]
