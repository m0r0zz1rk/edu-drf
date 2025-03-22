import uuid

from django.db.models import QuerySet

from apps.commons.utils.django.response import response_utils
from apps.guides.selectors.oo import oo_queryset, oo_orm
from apps.guides.services.mo import mo_service
from apps.guides.services.oo_type import oo_type_service


class OoService:
    """Класс методов для работы с ОО"""

    @staticmethod
    def get_mo_oos(mo_id: uuid) -> QuerySet:
        """
        Получение списка ОО для конкретного МО
        :param mo_id: object_id МО
        :return: QuerySet с попадающими под параметры ОО
        """
        return oo_queryset().filter(mo_id=mo_id).order_by('short_name')

    @staticmethod
    def generate_oo_process_data(serialize_data: dict) -> dict:
        """
        Формирование словаря данных для отправки в ORM для выполнения запроса
        :param serialize_data: Словарь данных из сериализатора
        :return: Словарь c подготовленным к передаче в ORM данными
        """
        process_data = serialize_data
        for key in process_data.keys():
            if key == 'mo':
                process_data[key] = mo_service.get_mo_object_by_name(serialize_data.get(key))
            if key == 'oo_type':
                process_data[key] = oo_type_service.get_oo_type_object_by_name(serialize_data.get(key))
        return process_data

    def create_oo(self, serialize_data: dict):
        """
        Создание образовательной организации
        :param serialize_data: Словарь с информацией об ОО (OoCreateSerializer)
        :return:
        """
        process_data = self.generate_oo_process_data(serialize_data)
        oo_orm.create_record(process_data)
        return response_utils.ok_response('Добавление выполнено')

    def update_oo(self, serialize_data: dict):
        """
        Обновление образовательной организации
        :param serialize_data: Словарь с информацией об ОО (OoUpdateSerializer)
        :return:
        """
        process_data = self.generate_oo_process_data(serialize_data)
        object_id = process_data.get('object_id')
        del process_data['object_id']
        oo_orm.update_record({'object_id': object_id}, process_data)
        return response_utils.ok_response('Обновление выполнено')


oo_service = OoService()
