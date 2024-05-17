from django.urls import path

from apps.commons.api.ad_centre_viewset import AdCentreViewSet

urlpatterns = [
    path('ad_centres/', AdCentreViewSet.as_view({'get': 'list'}))
]
