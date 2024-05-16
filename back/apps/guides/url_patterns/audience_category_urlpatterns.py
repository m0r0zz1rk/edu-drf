from django.urls import path

from apps.guides.api.audience_category_viewset import AudienceCategoryViewSet

audience_category_urlpatterns = [
    path('audience_categories/', AudienceCategoryViewSet.as_view({'get': 'list'})),
    path('audience_category/create/', AudienceCategoryViewSet.as_view({'post': 'create'})),
    path('audience_category/update/', AudienceCategoryViewSet.as_view({'patch': 'update'})),
    path('audience_category/delete/<uuid:object_id>/', AudienceCategoryViewSet.as_view({'delete': 'destroy'}))
]