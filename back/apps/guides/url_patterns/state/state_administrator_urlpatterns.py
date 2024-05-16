from django.urls import path

from apps.guides.api.state.state_administrator_viewset import StateAdministratorViewSet

state_administrator_urlpatterns = [
    path('admin_states/', StateAdministratorViewSet.as_view({'get': 'list'})),
    path('admin_state/create/', StateAdministratorViewSet.as_view({'post': 'create'})),
    path('admin_state/update/', StateAdministratorViewSet.as_view({'patch': 'update'})),
    path('admin_state/delete/<uuid:object_id>/', StateAdministratorViewSet.as_view({'delete': 'destroy'}))
]
