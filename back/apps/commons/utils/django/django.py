from typing import Optional, Union

from django.conf import settings


class DjangoUtils:
    """Класс методов для работы с элементами Django"""

    @staticmethod
    def is_settings_parameter_exists(param: str) -> bool:
        """Проверка на существующий в settings параметр"""
        if hasattr(settings, param):
            return True
        return False

    def get_parameter_from_settings(self, param: str) -> Optional[Union[str, int, float, list]]:
        """Получение значения параметра из settings"""
        if self.is_settings_parameter_exists(param):
            return getattr(settings, param, None)
        return None
