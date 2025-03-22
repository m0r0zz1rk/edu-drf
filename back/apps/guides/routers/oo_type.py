from apps.commons.drf.routers.LCUDE_router import ListCreateUpdateDeleteExportRouter
from apps.guides.api.oo_type import OoTypeViewSet

oo_type_router = ListCreateUpdateDeleteExportRouter(trailing_slash=True)
oo_type_router.register('oo_type', OoTypeViewSet)
