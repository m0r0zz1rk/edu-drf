from apps.commons.drf.routers.L_router import ListRouter
from apps.guides.api.state.state_registration import StateRegistrationViewSet

state_registration_router = ListRouter(trailing_slash=True)
state_registration_router.register('state', StateRegistrationViewSet)
