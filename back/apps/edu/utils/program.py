from typing import Optional

from django.apps import apps

from apps.commons.utils.ad.ad_centre import AdCentreUtils
from apps.commons.utils.data_types.file import FileUtils
from apps.commons.utils.django.exception import ExceptionHandling

program_model = apps.get_model('edu', 'Program')

class ProgramUtils:
    """Класс действия для работы с ДПП"""

    @staticmethod
    def is_program_exists(attribute_name: str, value: str) -> bool:
        """
        Проверка на существующую ДПП
        :param attribute_name: Наименование поля модели Program
        :param value: значение
        :return: True - существует, False - не существует
        """
        try:
            find = {attribute_name: value}
            return program_model.objects.filter(**find).exists()
        except:
            return False

    def get_order_file(self, attribute_name: str, value: str):
        """
        Получение файла приказа ДПП для найденного ДПП
        :param attribute_name: поле модели Program
        :param value: значение
        :return: str - путь до файла приказа, None - ошибка при получении пути
        """
        try:
            if self.is_program_exists(attribute_name, value):
                find = {attribute_name: value}
                program = program_model.objects.filter(**find).first()
                if program.program_order is not None:
                    return program.program_order.file
            return None
        except:
            return None

    @staticmethod
    def transform_instance_to_serializer(instance: program_model) -> Optional[dict]:
        """
        Преобразование ДПП в вид сериалайзера ProgramAddSerializer
        :param instance: объект модели program_model
        :return: dict - словарь с данными ДПП, None - ошибка при преобразовании
        """
        try:
            data = {}
            for key, value in instance.__dict__.items():
                if key not in [
                    '_state',
                    'department_id',
                    'program_order_id',
                    'categories',
                    'program_order'
                ]:
                    data[key] = value
            dep = AdCentreUtils().get_ad_centre('object_id', instance.department_id)
            data['department'] = dep.display_name
            data['order_id'] = None
            data['order_number'] = None
            data['order_date'] = None
            data['order_file'] = None
            if instance.program_order:
                data['order_id'] = instance.program_order.object_id
                data['order_number'] = instance.program_order.number
                data['order_date'] = instance.program_order.date
                if instance.program_order.file:
                    data['order_file'] = instance.program_order.file
            categories = ''
            for category in instance.categories.all():
                categories += f'{category.name}, '
            data['categories'] = categories[:-2]
            return data
        except Exception:
            return None
