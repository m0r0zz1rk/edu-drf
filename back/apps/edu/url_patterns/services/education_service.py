from django.urls import path

from apps.edu.api.services.education_service import EducationServiceViewSet

education_service_urlpatterns = [
    path('education_services/', EducationServiceViewSet.as_view({'get': 'list'})),
    path('education_service/<uuid:object_id>/', EducationServiceViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    })),
    path('education_service/', EducationServiceViewSet.as_view({'post': 'create_update'})),
]
