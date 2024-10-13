from django.urls import path

from apps.guides.api.position_category import PositionCategoryViewSet

position_category_urlpatterns = [
    path('position_categories/', PositionCategoryViewSet.as_view({'get': 'list'})),
    path('position_category/create/', PositionCategoryViewSet.as_view({'post': 'create'})),
    path('position_category/update/', PositionCategoryViewSet.as_view({'patch': 'update'})),
    path('position_category/delete/<uuid:object_id>/', PositionCategoryViewSet.as_view({'delete': 'destroy'}))
]
