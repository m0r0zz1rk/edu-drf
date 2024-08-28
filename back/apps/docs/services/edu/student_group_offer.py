import os

from apps.commons.utils.django.settings import SettingsUtils


class StudentGroupOfferService:
    """Класс методов для работы со сканами договоров оферты учебных групп"""

    su = SettingsUtils()

    def get_upload_path(self, instance, filename) -> str:
        """
        Получение пути загрузки файлов
        :param instance: сущность файла (получаем из FileField)
        :param filename: имя файла (получаем из FileField)
        :return: Путь для загрузки
        """
        _, file_extension = os.path.splitext(filename)
        new_file_name = f"{''.join(symb for symb in instance.number if symb == ' ' or symb.isalnum())}{file_extension}"
        order_path = self.su.get_parameter_from_settings('MEDIA_ROOT')
        for subfolder in ['Договора', 'Оферта', instance.student_group.code]:
            order_path = os.path.join(order_path, subfolder)
            if not os.path.exists(order_path):
                os.makedirs(order_path)
        return os.path.join(order_path, new_file_name)
