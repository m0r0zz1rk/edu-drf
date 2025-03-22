import datetime
import uuid

from django.core.files import File

from apps.docs.exceptions.program_order import ProgramOrderFieldNotFound
from apps.docs.selectors.program_order import program_order_orm


class ProgramOrderService:
    """Класс методов для работы с приказами ДПП"""

    _update_required_fields = ('date', 'number')
    _create_required_fields = (*_update_required_fields, 'file')

    def _check_data_fields(self, keys: list, create: bool = True):
        """
        Проверка полученных полей с кортежем обязательных для процесса
        :param keys: список ключей словаря с данными по приказу
        :param create: булево - если True проверяем _create_required_fields, иначе _update_required_fields
        :return: если поле отсутствует - поднять исключение ProgramOrderFieldNotFound
        """
        fields = self._update_required_fields
        if create:
            fields = self._create_required_fields
        for field in fields:
            if field not in keys:
                e = ProgramOrderFieldNotFound()
                e.field_name = field
                raise e

    def create_program_order(self, order_data: dict) -> uuid.uuid4:
        """
        Добавление приказа ДПП
        :param order_data: Словарь с данными по приказу (ключи: date, number, file)
        :return: uuid4 созданной записи в БД
        """
        self._check_data_fields(list(order_data.keys()))
        new_order_id = uuid.uuid4()
        order_data['object_id'] = new_order_id
        if type(order_data['date']) is str:
            order_data['date'] = datetime.datetime.strptime(order_data['date'], '%Y-%m-%d')
        if type(order_data.get('file')) is str:
            path = order_data.get('file')
            del order_data['file']
            program_order_orm.create_record(order_data)
            program_order_orm.update_record({'object_id': new_order_id}, {'file': File(open(path, 'rb'))})
        else:
            program_order_orm.create_record(order_data)
        return new_order_id

    def update_program_order(self, order_id: uuid, order_data: dict):
        """
        Обновление приказа ДПП
        :param order_id: UUID приказа ДПП в БД
        :param order_data: Словарь с данными (ключи: date, number, file (опционально))
        :return: None
        """
        self._check_data_fields(list(order_data.keys()), False)
        if type(order_data['date']) is str:
            order_data['date'] = datetime.datetime.strptime(order_data['date'], '%Y-%m-%d')
        if 'file' in order_data.keys() and type(order_data['file']) is str:
            path = order_data.get('file')
            del order_data['file']
            program_order_orm.update_record(
                {'object_id': order_id},
                {**order_data, 'file': File(open(path, 'rb'))}
            )
        else:
            program_order_orm.update_record({'object_id': order_id}, order_data)


program_order_service = ProgramOrderService()
