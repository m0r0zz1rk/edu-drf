from rest_framework.permissions import IsAuthenticated

from apps.commons.drf.viewset.base_viewset import BaseViewSet
from apps.commons.permissions.is_admin_or_coko import IsAdminOrCoko
from apps.journal.consts.journal_modules import APPLICATIONS


class ApplicationsViewSet(BaseViewSet):
    """Класс эндпонитов для работы с заявками"""
    permission_classes = [IsAuthenticated, IsAdminOrCoko]
    module = APPLICATIONS
