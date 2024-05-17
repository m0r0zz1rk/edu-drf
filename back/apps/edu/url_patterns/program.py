from django.urls import path

from apps.edu.api.program_viewset import ProgramViewSet

program_urlpatterns = [
    path('programs/', ProgramViewSet.as_view({'get': 'list'}))
]
