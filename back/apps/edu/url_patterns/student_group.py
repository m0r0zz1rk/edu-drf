from django.urls import path

from apps.edu.api.student_group import StudentGroupViewSet

student_group_urlpatterns = [
    path('student_group/', StudentGroupViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('student_group/<uuid:object_id>/', StudentGroupViewSet.as_view({
        'get': 'retrieve',
        'patch': 'update',
        'delete': 'destroy'
    })),
    path('student_group_service_type/<uuid:object_id>/', StudentGroupViewSet.as_view({'get': 'get_service_type'}))
]
