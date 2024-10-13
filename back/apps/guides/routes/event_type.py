from django.urls import path

from apps.guides.api.event_type import EventTypeViewSet

event_type_urlpatterns = [
    path('event_types/', EventTypeViewSet.as_view({'get': 'list'})),
    path('event_type/create/', EventTypeViewSet.as_view({'post': 'create'})),
    path('event_type/update/', EventTypeViewSet.as_view({'patch': 'update'})),
    path('event_type/delete/<uuid:object_id>/', EventTypeViewSet.as_view({'delete': 'destroy'}))
]
