from apps.commons.drf.routers.LRU_router import ListRetrieveUpdateRouter
from apps.edu.api.planning_parameter import PlanningParameterViewSet

planning_parameter_router = ListRetrieveUpdateRouter(trailing_slash=True)
planning_parameter_router.register('planning_parameter', PlanningParameterViewSet)
