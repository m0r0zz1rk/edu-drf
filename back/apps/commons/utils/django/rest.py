from typing import Optional

from apps.commons.utils.data_types.dict import DictUtils


class RestUtils:
    """Валидаторы и методы для запросов"""

    def validate_params_to_list(self, request, available: list) -> bool:
        """Сверка получаемых параметров в запросе с заданным списком"""
        params = self.get_request_parameters(request)
        for k in params.keys():
            if k not in available:
                print(k)
                return False
        return True

    @staticmethod
    def get_request_parameters(request) -> dict:
        """Формирование словаря с параметрами из полученного запроса"""
        d = {}
        if request.data is None:
            d = request.query_params.dict()
        else:
            if isinstance(request.data, dict):
                d = request.data
            else:
                d = DictUtils.convert_obj_to_dict(request.data)
        return d

    @staticmethod
    def is_param_in_request(request, key: str) -> bool:
        """Проверка на наличие параметра в запросе"""
        return key in request.data

    def get_request_parameter_by_key(self, request, key: str) -> Optional[str]:
        """Получение значения параметра запроса по ключу"""
        if self.is_param_in_request(request, key):
            return request.data[key]
        else:
            return None

    @staticmethod
    def take_parameter_by_request_GET(request, key: str) -> Optional[str]:
        """Получение параметра из GET запроса"""
        if request.GET is not None:
            if key in request.GET:
                return request.GET[key]
        return None
