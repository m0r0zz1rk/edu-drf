from apps.commons.drf.viewset.base_viewset import BaseViewSet
from apps.journal.consts.journal_modules import APPLICATIONS


class ApplicationsViewSet(BaseViewSet):
    """Класс эндпонитов для работы с заявками"""
    module = APPLICATIONS
