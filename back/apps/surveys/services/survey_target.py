import uuid
from typing import Optional

from apps.surveys.consts.survey_target_types import SURVEY_TARGET_TYPES, NOT_SET, EDU, INFO, ALL
from apps.surveys.exceptions.survey_target import TargetInfoNotCorrect, TargetNotExists
from apps.surveys.selectors.survey_target import survey_target_model, survey_target_orm


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
    def check_special_survey_for_group(group_id: uuid) -> bool:
        """
        Проверка наличия специального опроса для учебной группы
        :param group_id: object_id учебной группы
        :return: True - опрос найден, False - опрос не найден
        """
        target = survey_target_orm.get_one_record_or_none(filter_by={'group_id': group_id})
        return target is not None

    def get_special_survey_id_for_group(self, group_id: uuid) -> Optional[uuid.uuid4]:
        """
        Получение object_id специального опроса для учебной группы (при наличии)
        :param group_id: object_id учебной группы
        :return: object_id опроса или None, если такой опрос не существует
        """
        if self.check_special_survey_for_group(group_id):
            target = survey_target_orm.get_one_record_or_none(filter_by={'group_id': group_id})
            return target.object_id

    @staticmethod
    def check_service_survey_for_type(survey_type: SURVEY_TARGET_TYPES) -> bool:
        """
        Проверка наличия опроса по услуге
        :param survey_type: тип опроса (EDU или INFO)
        :return: True - опрос найден, False - опрос не найден
        """
        survey = survey_target_orm.get_one_record_or_none(filter_by={'type': survey_type})
        return survey is not None

    def get_service_survey_id_for_group(self, group_type: str) -> Optional[uuid.uuid4]:
        """
        Получение опроса по услуге
        :param group_type: тип услуги учебной группы (ou или iku)
        :return: object_id опроса или None, если опроса по услуге нет
        """
        survey_type = EDU if group_type == 'ou' else INFO
        if self.check_service_survey_for_type(survey_type):
            target = survey_target_orm.get_one_record_or_none(filter_by={'type': survey_type})
            return target.object_id

    @staticmethod
    def get_all_survey_id() -> uuid:
        """
        Получение object_id для опроса для всех групп
        :return: object_id опроса
        """
        target = survey_target_orm.get_one_record_or_none(filter_by={'type': ALL})
        return target.survey_id

    @staticmethod
    def remove_exist_survey_type(survey_type: str):
        """
        Удаление полученного типа таргетирования у существующих записей в БД
        :param survey_type: Тип таргетирования
        """
        if survey_type in ['all', 'edu', 'info']:
            targets = survey_target_orm.get_filter_records(filter_by={'type': survey_type})
            for target in targets:
                survey_target_orm.update_record(
                    filter_by={'object_id': target.object_id},
                    update_object={'type': NOT_SET}
                )

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
        survey_target_orm.update_record(
            filter_by={'object_id': obj_id},
            update_object=target_info
        )

    def delete_survey_target(self, target_id: uuid):
        """
        Удаление назначения опроса
        :param target_id: object_id объекта назнанчения
        """
        try:
            survey_target_orm.delete_record(filter_by={'object_id': target_id})
        except Exception:
            raise TargetNotExists


survey_target_service = SurveyTargetService()
