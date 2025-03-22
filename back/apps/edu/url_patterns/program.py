from django.urls import path

from apps.commons.drf.routers.LRCUDE_router import ListRetrieveCreateUpdateDeleteExportRouter
from apps.edu.api.program import ProgramViewSet

program_router = ListRetrieveCreateUpdateDeleteExportRouter(trailing_slash=True)
program_router.register('program', ProgramViewSet)

program_urlpatterns = [
    path('approved_program/', ProgramViewSet.as_view({'get': 'approved_list'})),
    path('program/copy/<uuid:object_id>/', ProgramViewSet.as_view({'get': 'copy'})),
    path('program/set_kug_edit/<uuid:program_id>/', ProgramViewSet.as_view({'get': 'set_kug_edit'})),
    path('program/order_file/<uuid:order_id>/', ProgramViewSet.as_view({'get': 'get_order_file'})),
    path('program/delete/<uuid:object_id>/', ProgramViewSet.as_view({'delete': 'destroy'}))
]

program_urlpatterns += program_router.urls
