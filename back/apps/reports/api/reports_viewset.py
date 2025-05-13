from apps.commons.drf.viewset.base_viewset import BaseViewSet
from apps.journal.consts.journal_modules import REPORTS


class ReportsViewSet(BaseViewSet):
    """Класс эндпоинтов для работы с учебной частью"""
    module = REPORTS
