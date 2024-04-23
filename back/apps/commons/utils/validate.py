import uuid


class ValidateUtils:
    """Класс методов для валидации данных"""

    @staticmethod
    def validate_data(fields: list, data: dict) -> bool:
        """
        Валидация полученных данных с полями модели
        :param fields: Список полей модели
        :param data: Входные данные в формате словаря
        :return: true - данные валидны, false - данные не валидны
        """
        for k in data.keys():
            if k not in fields:
                return False
        return True

    @staticmethod
    def validate_uuid(text) -> bool:
        """
        Проверка является ли получаемая переменная uuid
        :param text: переменная
        :return: true - является, false - не является
        """
        try:
            uuid.UUID(str(text))
            return True
        except ValueError:
            return False
