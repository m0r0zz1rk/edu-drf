from django.urls import path

from apps.applications.api.event_application.admin import EventApplicationAdminViewSet
from apps.commons.drf.routers.LRUD_router import ListRetrieveUpdateDeleteRouter

event_application_admin_router = ListRetrieveUpdateDeleteRouter(trailing_slash=True)
event_application_admin_router.register('event_application_admin', EventApplicationAdminViewSet)

urlpatterns = [
    path('event_pay_denied/<uuid:object_id>/', EventApplicationAdminViewSet.as_view({'post': 'pay_denied'})),
    path('event_one_move/', EventApplicationAdminViewSet.as_view({'post': 'one_move'})),
    path('event_all_move/', EventApplicationAdminViewSet.as_view({'post': 'all_move'})),
]

urlpatterns += event_application_admin_router.urls
