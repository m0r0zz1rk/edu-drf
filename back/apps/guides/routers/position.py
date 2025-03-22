from apps.commons.drf.routers.LCUDE_router import ListCreateUpdateDeleteExportRouter
from apps.guides.api.position import PositionViewSet

position_router = ListCreateUpdateDeleteExportRouter(trailing_slash=True)
position_router.register('position', PositionViewSet)
