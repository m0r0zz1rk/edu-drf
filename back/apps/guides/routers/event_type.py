from apps.commons.drf.routers.LCUDE_router import ListCreateUpdateDeleteExportRouter
from apps.guides.api.event_type import EventTypeViewSet

event_type_router = ListCreateUpdateDeleteExportRouter(trailing_slash=True)
event_type_router.register('event_type', EventTypeViewSet)

