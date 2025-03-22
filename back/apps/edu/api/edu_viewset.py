from apps.commons.drf.viewset.base_viewset import BaseViewSet
from apps.journal.consts.journal_modules import EDU


class EduViewSet(BaseViewSet):
    """Класс эндпоинтов для работы с учебной частью"""
    module = EDU
