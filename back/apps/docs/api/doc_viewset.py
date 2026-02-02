from rest_framework import permissions

from apps.commons.drf.viewset.base_viewset import BaseViewSet
from apps.commons.permissions.is_admin_or_coko import IsAdminOrCoko
from apps.journal.consts.journal_modules import DOCS


class DocsViewSet(BaseViewSet):
    """
    Класс вьюсета для документов
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrCoko]
    module = DOCS
