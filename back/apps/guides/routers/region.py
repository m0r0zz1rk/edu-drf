from apps.commons.drf.routers.LCUDE_router import ListCreateUpdateDeleteExportRouter
from apps.guides.api.region import RegionViewSet

region_router = ListCreateUpdateDeleteExportRouter(trailing_slash=True)
region_router.register('region', RegionViewSet)
