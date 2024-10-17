import uuid

from apps.surveys.consts.survey_target_types import SURVEY_TARGET_TYPES, NOT_SET
from apps.surveys.exceptions.survey_target import TargetInfoNotCorrect, TargetNotExists
from apps.surveys.selectors.survey_target import survey_target_model


class SurveyTargetService:
    """Класс методов для работы с назначениями опросов"""

    _survey_target_required_keys = [
        'object_id',
        'survey_id',
        'type'
    ]

    def check_survey_target_info(self, target_info: dict) -> bool:
        """
        Структурная проверка полученной информации по назначению опроса
        :param target_info: информация по назначению опроса
        :return: True - проверка пройдена, False - проверка не пройдена
        """
        for key in self._survey_target_required_keys:
            if key not in target_info:
                return False
        return True

    @staticmethod
    def remove_exist_survey_type(type: str):
        """
        Удаление полученного типа таргетирования у существующих записей в БД
        :param type: Тип таргетирования
        """
        if type in ['all', 'edu', 'info']:
            for target in (survey_target_model.objects.
                           select_related('survey').
                           select_related('group').
                           filter(type=type)):
                target.type = NOT_SET
                target.save()

    def add_edit_survey_target(self, target_info: dict):
        """
        Добавление/Изменение назначения опроса
        :param target_info: информация по назначению опроса
        """
        if not self.check_survey_target_info(target_info):
            raise TargetInfoNotCorrect
        for target_type in SURVEY_TARGET_TYPES:
            if target_type[1] == target_info['type']:
                target_info['type'] = target_type[0]
        self.remove_exist_survey_type(target_info['type'])
        obj_id = target_info['object_id']
        del target_info['object_id']
        survey_target_model.objects.update_or_create(
            object_id=obj_id,
            defaults=target_info
        )

    def delete_survey_target(self, target_id: uuid):
        """
        Удаление назначения опроса
        :param target_id: object_id объекта назнанчения
        """
        try:
            survey_target_model.objects.get(object_id=target_id).delete()
        except Exception:
            raise TargetNotExists
