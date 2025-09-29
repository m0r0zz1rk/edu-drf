from typing import Optional

from apps.guides.operations.add_update_guides_rec import AddUpdateGuidesRec
from apps.guides.selectors.state import state_model, state_orm

default_states = [
    'Россия',
    'Украина',
    'Беларусь',
    'Казахстан'
]


class StateService:
    """Класс методов для работы с государствами"""

    @staticmethod
    def is_state_exist(attribute_name: str, value: str) -> bool:
        """
        Проверка на существующее государство в БД
        :param attribute_name: наименование атрибута (поля модели State)
        :param value: значение
        :return: true - государство существует, false - государство не существует
        """
        find = {attribute_name: value}
        state = state_orm.get_one_record_or_none(filter_by=find)
        return state is not None

    def add_based_states(self):
        """Добавление базовых государств (с проверкой на существующие)"""
        for state in default_states:
            if not self.is_state_exist('name', state):
                AddUpdateGuidesRec(
                    'State',
                    {'name': state}
                )

    def get_state_by_name(self, name: str) -> Optional[state_model]:
        """
        Получение сущности государства по object_id
        :param name: название государства
        :return: None - государство не найдено, state_model - сущность государства
        """
        if self.is_state_exist('name', name):
            return state_orm.get_one_record_or_none(filter_by={'name': name})
        return None
