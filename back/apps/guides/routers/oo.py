from apps.commons.drf.routers.LCUDE_router import ListCreateUpdateDeleteExportRouter
from apps.guides.api.oo import OoViewSet

oo_router = ListCreateUpdateDeleteExportRouter(trailing_slash=True)
oo_router.register('oo', OoViewSet)
