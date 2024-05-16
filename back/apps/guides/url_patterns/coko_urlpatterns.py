from django.urls import path

from apps.guides.api.coko_viewset import CokoViewSet

coko_urlpatterns = [
    path('cokos/', CokoViewSet.as_view({'get': 'list'})),
    path('coko/change_curator_groups/', CokoViewSet.as_view({'post': 'change_curator_groups'})),
]
