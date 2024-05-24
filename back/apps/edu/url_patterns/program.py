from django.urls import path

from apps.edu.api.program_viewset import ProgramViewSet

program_urlpatterns = [
    path('programs/', ProgramViewSet.as_view({'get': 'list'})),
    path('program/create/', ProgramViewSet.as_view({'post': 'create'})),
    path('program/order_file/<uuid:order_id>/', ProgramViewSet.as_view({'get': 'get_order_file'}))
]
