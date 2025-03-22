from django.urls import path

from apps.guides.api.profiles.coko import CokoViewSet

coko_urlpatterns = [
    path('coko/', CokoViewSet.as_view({'get': 'list'})),
    path('coko/change_curator_groups/', CokoViewSet.as_view({'post': 'change_curator_groups'})),
]
