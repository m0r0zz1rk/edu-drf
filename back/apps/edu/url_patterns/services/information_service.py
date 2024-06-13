from django.urls import path

from apps.edu.api.services.information_service import InformationServiceViewSet

information_service_urlpatterns = [
    path('information_services/', InformationServiceViewSet.as_view({'get': 'list'})),
    path('information_service/<uuid:object_id>/', InformationServiceViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    })),
    path('information_service/', InformationServiceViewSet.as_view({'post': 'create_update'})),
]
