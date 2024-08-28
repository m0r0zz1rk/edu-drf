from typing import Optional

from apps.edu.selectors.planning_parameter import planning_parameter_model


class PlanningParameterService:
    """Класс методов для работы с параметрами планирования"""

    @staticmethod
    def is_parameter_exist(attribute_name: str, value: str) -> bool:
        """
        Проверка на существующий параметр планирования
        :param attribute_name: имя атрибута для поиска (object_id, name, description)
        :param value: значение атрибута
        :return: True - параметр существует, False - параметр не существует
        """
        find = {attribute_name: value}
        return planning_parameter_model.objects.filter(**find).exists()

    def get_planning_parameter(self, attribute_name: str, value: str) -> Optional[planning_parameter_model]:
        """
        Получение параметра планирования
        :param attribute_name: имя атрибута для поиска (object_id, name, description)
        :param value: значение атрибута
        :return: None - параметр не найден, planning_parameter_model - объект параметра
        """
        if self.is_parameter_exist(attribute_name, value):
            find = {attribute_name: value}
            return planning_parameter_model.objects.filter(**find).first()
        return None
