from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.commons.pagination import CustomPagination
from apps.guides.filters.state_filter import StateFilter
from apps.guides.serializers.state.state_administrator_serilaizer import state_model, StateAdministratorSerializer


class StateAdministratorViewSet(viewsets.ModelViewSet):
    """Работа с государствами в модуле Справочников"""
    queryset = state_model.objects.all().order_by('name')
    serializer_class = StateAdministratorSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = StateFilter
