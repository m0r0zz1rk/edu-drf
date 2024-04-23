from datetime import date
from typing import Optional

from apps.commons.utils.data_types.date import DateUtils


class DictUtils:
    """Словарные валидаторы и методы"""

    @staticmethod
    def dict_is_empty(d: dict) -> bool:
        """Проверка на пустой словарь"""
        if not bool(d):
            return True
        else:
            return False

    @staticmethod
    def exist_key_in_dict(key: str, data: dict) -> bool:
        """Проверка нахождения ключа в словаре"""
        if data is None:
            return False
        if key in data.keys():
            return True
        else:
            return False

    def get_str_value_in_dict_by_key(self,
                                     key: str,
                                     data: dict,
                                     default=None) -> Optional[str]:
        """Получение строки по ключу в словаре"""
        if self.exist_key_in_dict(key, data):
            value = data[key]
            if value is not None:
                if isinstance(value, str):
                    if value != 'null':
                        return value
                    return None
                else:
                    try:
                        return str(value)
                    except ValueError:
                        return default
            return None
        return default

    def get_int_value_in_dict_by_key(self,
                                     key: str,
                                     data: dict,
                                     default=None) -> int:
        """Получение числа по ключу в словаре"""
        if self.exist_key_in_dict(key, data):
            value = data[key]
            if value is None:
                return default
            if isinstance(value, int):
                return value
            else:
                try:
                    return int(value)
                except ValueError:
                    return default
        return default

    def get_float_value_in_dict_by_key(self,
                                       key: str,
                                       data: dict,
                                       default=None) -> float:
        """Получение дробного числа по ключу в словаре"""
        if self.exist_key_in_dict(key, data):
            value = data[key]
            if value is None:
                return default
            if isinstance(value, float):
                return value
            else:
                try:
                    return float(value)
                except ValueError:
                    return default
        return default

    def get_date_value_in_dict_by_key(self,
                                      key: str,
                                      data: dict,
                                      default=None) -> Optional[date]:
        """Получение даты по ключу в словаре"""
        if self.exist_key_in_dict(key, data):
            value = data[key]
            if value is not None:
                if type(value) == date:
                    return value
                else:
                    try:
                        return value.date()
                    except AttributeError:
                        try:
                            return DateUtils.convert_html_date(value)
                        except Exception:
                            return default
                    except ValueError:
                        return default
            return None
        return default

    def get_file_in_dict_by_key(self,
                                key: str,
                                data: dict,
                                default=None):
        """Получение файла по ключу в словаре"""
        if self.exist_key_in_dict(key, data):
            value = data[key]
            if value is not None:
                return value
            return None
        return default

    def get_value_in_dict_by_key(self,
                                 key: str,
                                 data: dict,
                                 default=None) -> str:
        """Получение значения по ключу в словаре"""
        if self.exist_key_in_dict(key, data):
            value = data[key]
            return value
        return default

    def get_dictionary_in_dict_by_key(self,
                                      key: str,
                                      data: dict,
                                      default={}) -> dict:
        """Получение словаря по ключу в словаре"""
        if self.exist_key_in_dict(key, data):
            value = data[key]
            return value
        return default

    def get_list_in_dict_by_key(self,
                                key: str,
                                data: dict,
                                default=[]) -> list:
        """Получение словаря по ключу в словаре"""
        if self.exist_key_in_dict(key, data):
            value = data[key]
            return value
        return default

    @staticmethod
    def convert_obj_to_dict(obj):
        """Конвертирование объекта в словарь"""
        try:
            return dict(obj)
        except ValueError:
            return None
