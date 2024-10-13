from django.urls import path

from apps.guides.api.region import RegionViewSet

region_urlpatterns = [
    path('regions/', RegionViewSet.as_view({'get': 'list'})),
    path('region/create/', RegionViewSet.as_view({'post': 'create'})),
    path('region/update/', RegionViewSet.as_view({'patch': 'update'})),
    path('region/delete/<uuid:object_id>/', RegionViewSet.as_view({'delete': 'destroy'}))
]
