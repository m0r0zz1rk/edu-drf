from django.urls import path

from apps.guides.api.position import PositionViewSet

position_urlpatterns = [
    path('positions/', PositionViewSet.as_view({'get': 'list'})),
    path('position/create/', PositionViewSet.as_view({'post': 'create'})),
    path('position/update/', PositionViewSet.as_view({'patch': 'update'})),
    path('position/delete/<uuid:object_id>/', PositionViewSet.as_view({'delete': 'destroy'}))
]
