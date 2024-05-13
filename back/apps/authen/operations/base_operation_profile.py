from abc import ABC, abstractmethod

from apps.authen.utils.profile import ProfileUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.journal.consts.journal_modules import AUTHEN
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.utils.journal_utils import JournalUtils


class BaseOperationProfile(ABC):
    """Базовый класс для действий с профилями пользователей и сотрудников"""

    ju = JournalUtils()
    pu = ProfileUtils()
    model_name = source = module = ''
    object_data = request = None
    error = False

    def __init__(self, model_name: str, object_data: dict, request=None):
        """
        Инициализация класса
        :param model_name: наименование модели
        :param object_data: словарь с данными по редактируемому объекту
        :param request: объект request если запрос на добавление поступил через endpoint
        """
        self.model_name = model_name
        self.object_data = object_data
        if request is not None:
            self.request = request
        self._process()

    def _process(self):
        """Процесс работы с записью"""
        self.source = 'Администратор АИС'
        self.module = AUTHEN
        if self.request is not None:
            self.source = self.pu.get_profile_or_info_by_attribute(
                'django_user_id',
                self.request.user.id,
                'display_name'
            )
        try:
            complete = self.action()
            if not complete:
                self.error = False
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Процесс обновления профиля',
                    'module': AUTHEN,
                    'status': ERROR,
                    'description': 'Системная ошибка в процессе обновления профиля пользователя'
                },
                repr({
                    'source': self.source,
                    'module': self.module,
                    'object_data': self.object_data
                }),
                ExceptionHandling.get_traceback()
            )
            self.error = False


    @abstractmethod
    def action(self):
        """Действие"""
        pass