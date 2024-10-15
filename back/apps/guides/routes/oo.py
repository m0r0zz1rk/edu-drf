from django.urls import path

from apps.guides.api.oo import OoViewSet

oo_urlpatterns = [
    path('oos/', OoViewSet.as_view({'get': 'list'})),
    path('oo/create/', OoViewSet.as_view({'post': 'create'})),
    path('oo/update/', OoViewSet.as_view({'patch': 'update'})),
    path('oo/delete/<uuid:object_id>/', OoViewSet.as_view({'delete': 'destroy'}))
]
