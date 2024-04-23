class ListUtils:
    """Методы и валиадаторы при работе со списками"""

    @staticmethod
    def is_list_empty(l: list) -> bool:
        """Проверка на пустоту листа"""
        if l is not None and len(l) == 0:
            return True
        return False

    @staticmethod
    def is_dict_keys_valid_list(data: dict, value_list: list) -> bool:
        """Проверка на полное совпадение значений ключей словаря и списка"""
        for k in data.keys():
            if k not in value_list:
                return False
        return True

    @staticmethod
    def is_el_in_list(l: list, el: object) -> bool:
        """Проверка на наличие объекта в списке"""
        return el in l
