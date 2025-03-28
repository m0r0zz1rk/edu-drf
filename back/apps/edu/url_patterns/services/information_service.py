from apps.commons.drf.routers.LRCUDE_router import ListRetrieveCreateUpdateDeleteExportRouter
from apps.edu.api.services.information_service import InformationServiceViewSet

information_service_router = ListRetrieveCreateUpdateDeleteExportRouter(trailing_slash=True)
information_service_router.register('information_service', InformationServiceViewSet)
