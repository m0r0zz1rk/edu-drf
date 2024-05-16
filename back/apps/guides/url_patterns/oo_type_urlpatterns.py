from django.urls import path

from apps.guides.api.oo_type_viewset import OoTypeViewSet

oo_type_urlpatterns = [
    path('oo_types/', OoTypeViewSet.as_view({'get': 'list'})),
    path('oo_type/create/', OoTypeViewSet.as_view({'post': 'create'})),
    path('oo_type/update/', OoTypeViewSet.as_view({'patch': 'update'})),
    path('oo_type/delete/<uuid:object_id>/', OoTypeViewSet.as_view({'delete': 'destroy'}))
]
