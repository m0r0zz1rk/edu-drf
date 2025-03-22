from apps.commons.drf.routers.LCUDE_router import ListCreateUpdateDeleteExportRouter
from apps.guides.api.mo import MoViewSet

mo_router = ListCreateUpdateDeleteExportRouter(trailing_slash=True)
mo_router.register('mo', MoViewSet)
