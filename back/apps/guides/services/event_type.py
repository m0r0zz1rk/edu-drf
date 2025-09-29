from typing import Union

from apps.guides.selectors.event_type import event_type_model, event_type_orm


class EventTypeService:
    """Класс действия для работы с типами мероприятий"""

    @staticmethod
    def is_event_type_exist(attribute: str, value: str) -> bool:
        """
        Проверка на существующий тип мероприятий
        :param attribute: поле модели EventType
        :param value: значение атрибута
        :return: True - существует, False - не существует
        """
        find = {attribute: value}
        event_type = event_type_orm.get_filter_records(filter_by=find)
        return event_type is not None

    def get_event_type_object_by_name(self, name: str) -> Union[event_type_model, None]:
        """
        Получение типа мероприятий по полученному наименованию
        :param name: наименование типа мероприятий
        :return: Объект EventType (если не найдено - None)
        """
        if self.is_event_type_exist('name', name):
            return event_type_orm.get_one_record_or_none(filter_by={'name': name})
        return None


event_type_service = EventTypeService()
