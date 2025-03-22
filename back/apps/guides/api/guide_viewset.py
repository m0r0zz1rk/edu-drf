from apps.commons.drf.viewset.base_viewset import BaseViewSet
from apps.journal.consts.journal_modules import GUIDES


class GuideViewSet(BaseViewSet):
    """
    Класс вьюсета для справочников
    """
    module = GUIDES
