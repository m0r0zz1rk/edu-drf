from django.urls import path

from apps.commons.drf.routers.LRCUDE_router import ListRetrieveCreateUpdateDeleteExportRouter
from apps.edu.api.student_group import StudentGroupViewSet

student_group_router = ListRetrieveCreateUpdateDeleteExportRouter(trailing_slash=True)
student_group_router.register('student_group', StudentGroupViewSet)

student_group_urlpatterns = [
    path('student_group/doc/', StudentGroupViewSet.as_view({'post': 'doc'})),
    path('student_group/offer/', StudentGroupViewSet.as_view({'post': 'offer'}))
]

student_group_urlpatterns += student_group_router.urls
