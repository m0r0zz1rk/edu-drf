from typing import Optional

from django.apps import apps

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
