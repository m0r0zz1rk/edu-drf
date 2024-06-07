from django.urls import path

from apps.edu.api.program_viewset import ProgramViewSet

program_urlpatterns = [
    path('programs/', ProgramViewSet.as_view({'get': 'list'})),
    path('program/<uuid:object_id>/', ProgramViewSet.as_view({'get': 'retrieve'})),
    path('program/copy/<uuid:object_id>/', ProgramViewSet.as_view({'get': 'copy'})),
    path('program/set_kug_edit/<uuid:program_id>/', ProgramViewSet.as_view({'get': 'set_kug_edit'})),
    path('program/create_update/', ProgramViewSet.as_view({'post': 'create_update'})),
    path('program/order_file/<uuid:order_id>/', ProgramViewSet.as_view({'get': 'get_order_file'})),
    path('program/delete/<uuid:object_id>/', ProgramViewSet.as_view({'delete': 'destroy'}))
]
