import datetime
import uuid
from typing import Optional

from apps.commons.services.ad.ad_centre import ad_centre_service
from apps.edu.exceptions.planning_parameter.planning_days_error import PlanningDaysError
from apps.edu.selectors.services.information_service import information_service_model, information_service_orm
from apps.edu.services.planning_parameter import planning_parameter_service
from apps.guides.services.audience_category import audience_category_service
from apps.guides.services.event_type import event_type_service


class InformationServiceService:
    """Класс методов для работы с информационно-консультационными услугами (мероприятиями)"""

    @staticmethod
    def get_count() -> int:
        """
        Получение общего количества мероприятий в АИС
        """
        return information_service_orm.get_all_objects_count()

    @staticmethod
    def service_count(department: str) -> int:
        """
        Получение количества ОУ (курсов) для подразделения в текущем году
        :param department: display_name подразделения AD
        :return: количество ОУ (курсов)
        """
        services = information_service_orm.get_filter_records(
            filter_by={'department__display_name': department, 'date_start__year': datetime.datetime.now().year}
        )
        return services.count()

    @staticmethod
    def is_service_exists(attribute_name: str, value: str) -> bool:
        """
        Проверка на существующую ИКУ
        :param attribute_name: наименование поля модели InformationService
        :param value: значение
        :return: True - существует, False - не существует
        """
        find = {attribute_name: value}
        service = information_service_orm.get_one_record_or_none(filter_by=find)
        return service is not None

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
            service = information_service_orm.get_one_record_or_none(filter_by=find)
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
                service = information_service_orm.get_one_record_or_none(filter_by={'object_id': service_id})
                cats_str = ''
                for cat in service.categories.all().order_by('name'):
                    cats_str += f'{cat.name};; '
                res = {}
                for field in information_service_model._meta.concrete_fields:
                    res[field.name] = getattr(service, field.name)
                res['categories'] = cats_str[:-3]
                return res
            return None
        except Exception:
            return None

    @staticmethod
    def process_data_from_validated(
            validated_data: dict,
            service_id: uuid.uuid4 = None
    ) -> (dict, list):
        """
        Формирование словаря с готовыми для добавления или обновления данными
        на основе данных из сериализатора
        :param service_id: UUID сервиса
        :param validated_data: словарь валидированных данных из InformationServiceRetrieveAddUpdateSerializer
        :return: словарь с данными для ORM и список полученных категорий
        """
        process_data = dict(validated_data)
        if service_id:
            process_data['object_id'] = service_id
        event_type = event_type_service.get_event_type_object_by_name(validated_data.get('type'))
        process_data['type_id'] = event_type.object_id
        del process_data['type']
        department = ad_centre_service.get_ad_centre('display_name', validated_data.get('department'))
        process_data['department_id'] = department.object_id
        del process_data['department']
        data_categories = validated_data.get('categories').split(';;') \
            if len(validated_data.get('categories')) > 0 else []
        del process_data['categories']
        return process_data, data_categories

    @staticmethod
    def update_service_categories(service_id: uuid.uuid4, data_categories: list):
        """
        Обновление категорий для мероприятия (ИКУ)
        :param service_id: UUID мероприятия в БД
        :param data_categories: список категорий
        :return:
        """
        if len(data_categories) > 0:
            categories = []
            for category in data_categories:
                audience_category = audience_category_service.get_category_object_by_name(category)
                if audience_category:
                    categories.append(audience_category)
            information_service_orm.clear_many_to_many({'object_id': service_id}, 'categories')
            information_service_orm.add_many_to_many({'object_id': service_id}, 'categories', categories)

    def create_service(self, validated_data: dict):
        """
        Создание мероприятия (ИКУ)
        :param validated_data: словарь валидированных данных из InformationServiceRetrieveAddUpdateSerializer
        :return:
        """
        object_id = uuid.uuid4()
        create_data, data_categories = self.process_data_from_validated(validated_data, object_id)
        if planning_parameter_service.check_planning_days(create_data.get('date_start')):
            information_service_orm.create_record(create_data)
        else:
            raise PlanningDaysError
        self.update_service_categories(object_id, data_categories)

    def update_service(self, service_id: uuid.uuid4, validated_data: dict):
        """
        Обновление мероприятия (ИКУ)
        :param service_id: UUID мероприятия в БД
        :param validated_data: словарь валидированных данных из InformationServiceRetrieveAddUpdateSerializer
        :return:
        """
        del validated_data['object_id']
        update_data, data_categories = self.process_data_from_validated(validated_data)
        if planning_parameter_service.check_planning_days(update_data.get('date_start')):
            information_service_orm.update_record({'object_id': service_id}, update_data)
        else:
            raise PlanningDaysError
        self.update_service_categories(service_id, data_categories)


information_service_service = InformationServiceService()
