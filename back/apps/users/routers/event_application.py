from apps.commons.drf.routers.LRCUD_router import (
    ListRetrieveCreateUpdateDeleteRouter)
from apps.users.api.application.event_application import EventApplicationViewSet

event_application_router = ListRetrieveCreateUpdateDeleteRouter(trailing_slash=True)
event_application_router.register('event_application', EventApplicationViewSet)
