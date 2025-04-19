from apps.commons.drf.viewset.base_viewset import BaseViewSet
from apps.journal.consts.journal_modules import DOCS


class DocsViewSet(BaseViewSet):
    """
    Класс вьюсета для документов
    """
    module = DOCS
