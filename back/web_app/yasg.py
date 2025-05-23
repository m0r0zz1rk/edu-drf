from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='COKO38 Education Centre DRF+Vite+Vue',
        description='Учебный центр ГАУ ИО ЦОПМКиМКО',
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('backend/swg/', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
]
