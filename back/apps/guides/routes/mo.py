from django.urls import path

from apps.guides.api.mo import MoViewSet

mo_urlpatterns = [
    path('mos/', MoViewSet.as_view({'get': 'list'})),
    path('mo/create/', MoViewSet.as_view({'post': 'create'})),
    path('mo/update/', MoViewSet.as_view({'patch': 'update'})),
    path('mo/delete/<uuid:object_id>/', MoViewSet.as_view({'delete': 'destroy'}))
]
