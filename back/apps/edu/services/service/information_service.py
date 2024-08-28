import datetime
import uuid
from typing import Optional

from apps.edu.selectors.services.information_service import information_service_model


class InformationServiceService:
    """Класс методов для работы с информационно-консультационными услугами (мероприятиями)"""

    @staticmethod
    def service_count(department: str) -> int:
        """
        Получение количества ОУ (курсов) для подразделения в текущем году
        :param department: display_name подразделения AD
        :return: количество ОУ (курсов)
        """
        return information_service_model.objects. \
            filter(
            department__display_name=department
        ).filter(
            date_start__year=datetime.datetime.now().year
        ).count()

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

    def get_info_by_service(self, attribute_name: str, value: str, info: str) -> Optional[str]:
        """
        Получение наименование подразделения AD из ДПП ОУ
        :param attribute_name: наименование атриубта для поиска
        :param value: значения атрибута
        :param info: информация (dep_name, service_name)
        :return: str - display_name подразделения AD, None - ОУ не найдена
        """
        if self.is_service_exists(attribute_name, value):
            find = {attribute_name: value}
            service = information_service_model.objects.filter(**find).first()
            if info == 'dep_name':
                return service.department.display_name
            elif info == 'date_start':
                return service.date_start.strftime('%d.%m.%Y')
            elif info == 'date_end':
                return service.date_end.strftime('%d.%m.%Y')
            else:
                return service.name
        return None

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
                for field in information_service_model._meta.concrete_fields:
                    res[field.name] = getattr(service, field.name)
                res['categories'] = cats_str[:-3]
                return res
            return None
        except:
            return None
