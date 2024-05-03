from abc import ABC, abstractmethod

from apps.commons.utils.django.request import RequestUtils
from apps.journal.consts.journal_modules import GUIDES


class BaseOperationGuide(ABC):
    """Базовый класс для действий со справочниками"""

    model_name = ''
    object_data = request = None
    error = False

    def __init__(self, model_name: str, object_data: dict, request=None):
        """
        Инициализация класса
        :param model_name: наименование модели
        :param object_data: словарь с данными по добавляемому/редактируемому объекту
        :param request: объект request если запрос на добавление поступил через endpoint
        """
        self.model_name = model_name
        self.object_data = object_data
        if request is not None:
            self.request = request
        self._process()

    def _process(self):
        """Процесс работы с записью"""
        source = 'Система'
        module = GUIDES
        if self.request is not None:
            source = RequestUtils.get_source_display_name(self.request)
        process_data = {
            'source': source,
            'module': module,
            'process_data': {
                'model_info': {
                    'app': 'guides',
                    'model_name': self.model_name
                },
                'object': self.object_data
            }
        }
        complete = self.action(process_data)
        if not complete:
            self.error = False

    @abstractmethod
    def action(self, process_data: dict):
        """Действие"""
        pass