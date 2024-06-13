import uuid
from typing import Optional

from django.apps import apps

information_service_model = apps.get_model('edu', 'InformationService')


class InformationServiceService:
    """Класс методов для работы с информационно-консультационными услугами (мероприятиями)"""

    @staticmethod
    def is_service_exists(attribute_name: str, value: str) -> bool:
        """
        Проверка на существующую ИКУ
        :param attribute_name: наименование поля модели InformationService
        :param value: значение
        :return: True - существует, False - не существует
        """
        find = {attribute_name: value}
        return information_service_model.objects.filter(**find).exists()

    def prepare_to_serialize(self, service_id: uuid) -> Optional[dict]:
        """
        Подготовка ИКУ к сериализации (преобразование категорий слушателей в строку)
        :param service_id: object_id категории
        :return: None - ошибка, dict - словарь с данными ИКУ
        """
        try:
            if self.is_service_exists('object_id', service_id):
                service = information_service_model.objects.filter(object_id=service_id).first()
                cats_str = ''
                for cat in service.categories.all().order_by('name'):
                    cats_str += f'{cat.name};; '
                res = {}
                for field in information_service_model._meta.get_fields():
                    if field.name != 'categories':
                        res[field.name] = getattr(service, field.name)
                    else:
                        res['categories'] = cats_str[:-3]
                return res
            return None
        except:
            return None