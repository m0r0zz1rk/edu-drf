import uuid
from typing import Optional

from apps.authen.services.profile import ProfileService
from apps.commons.services.ad.ad_centre import AdCentreService, ad_centre_service
from apps.docs.services.edu.program_order import program_order_service
from apps.edu.operations.program.add_update_program import AddUpdateProgramOperation
from apps.edu.selectors.program import program_model, program_orm
from apps.guides.services.audience_category import audience_category_service


class ProgramService:
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
        except Exception:
            return False

    def get_program(self, attribute_name: str, value: str) -> Optional[program_model]:
        """
        Получение ДПП
        :param attribute_name: имя поля модели Program
        :param value: значение
        :return: None - ДПП не найдена, Program - объект ДПП
        """
        if self.is_program_exists(attribute_name, value):
            find = {attribute_name: value}
            return program_model.objects.filter(**find).first()
        return None

    def copy_program(self, program_id: uuid) -> Optional[str]:
        """
        Создание копии ДПП
        :param program_id: uuid оригинальной ДПП
        :return: object_id новой ДПП или None
        """
        program = self.get_program('object_id', program_id)
        if program is None:
            return False
        fields = [f.name for f in program_model._meta.concrete_fields
                  if f.name not in ['object_id', 'date_create', 'program_order']]
        new_program = {
            'object_id': None
        }
        for field in fields:
            if field != 'categories':
                new_program[field] = getattr(program, field)
                if field == 'name':
                    new_program[field] += '_Копия'
        cats = ''
        for cat in program.categories.all():
            cats += cat.name + ','
        cats = cats[:-1]
        new_program['categories'] = cats
        new_program['order_id'] = None
        new_program['order_number'] = None
        new_program['order_date'] = None
        new_program['order_file'] = None
        if program.program_order:
            new_program['order_number'] = program.program_order.number
            new_program['order_date'] = program.program_order.date
            new_program['order_file'] = program.program_order.file.path
        proc = AddUpdateProgramOperation(new_program)
        if proc.process_completed:
            return proc.dpp.object_id
        else:
            return None

    def get_order_file(self, attribute_name: str, value: str):
        """
        Получение файла приказа ДПП для найденного ДПП
        :param attribute_name: поле модели Program
        :param value: значение
        :return: str - путь до файла приказа, None - ошибка при получении пути
        """
        try:
            program = self.get_program(attribute_name, value)
            if program is not None:
                if program.program_order is not None:
                    return program.program_order.file
            return None
        except Exception:
            return None

    @staticmethod
    def transform_instance_to_serializer(instance: program_model) -> dict:
        """
        Преобразование ДПП в вид сериалайзера ProgramAddSerializer
        :param instance: объект модели program_model
        :return: dict - словарь с данными ДПП
        """
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
        dep = AdCentreService().get_ad_centre('object_id', instance.department_id)
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
            categories += f'{category.name};; '
        data['categories'] = categories[:-3]
        return data

    def set_kug_edit(self, program_id: uuid, user_id: int) -> bool:
        """
        Установить пользователя, редактирующего КУГ ДПП
        :param program_id: object_id ДПП
        :param user_id: ID пользователя Django
        :return: True - пользователь установлен, False - пользователь не установлен
        """
        program = self.get_program('object_id', program_id)
        if program is None:
            return False
        coko_profile = ProfileService().get_profile_or_info_by_attribute(
            'django_user_id',
            user_id,
            'profile'
        )
        if coko_profile is None:
            return False
        if program.kug_edit_id == coko_profile.object_id:
            program.kug_edit = None
        else:
            program.kug_edit_id = coko_profile.object_id
        program.save()
        return True

    @staticmethod
    def create_program(request, serialize_data: dict, create: bool = True):
        """
        Создание объекта ДПП
        :param request: Объект запроса в DRF
        :param serialize_data: Словарь с сериализованными данными (ProgramRetrieveAddUpdateSerializer)
        :param create: булево: если True, то выполняем добавление, иначе - обновление
        :return:
        """
        create_data = dict(serialize_data)
        for key in ('object_id', 'order_id', 'order_number', 'order_date', 'order_file'):
            del create_data[key]

        # Проверяем наличие файла с полученных данных - если есть, то вытаскиваем из request
        order_file = None
        if serialize_data.get('order_file') is not None:
            order_file = request.FILES['order_file']

        # Получаем наименование центра из AD
        create_data['department'] = ad_centre_service.get_ad_centre(
            'display_name',
            serialize_data['department']
        )

        # Получаем категории слушателей - со стороны фронта получаем категории текстом с разделителем ;;
        categories = []
        if len(serialize_data['categories']) > 0:
            categories = [
                audience_category_service.get_category_object_by_name(category_name).object_id
                for category_name in serialize_data.get('categories').split(';;')
                if audience_category_service.get_category_object_by_name(category_name) is not None
            ]
            del create_data['categories']

        # Обновляем информацию по приказу ДПП
        if serialize_data['order_id'] in [None, 'null']:
            if serialize_data['order_number'] is not None:
                create_data['program_order_id'] = program_order_service.create_program_order(
                    {
                        'number': serialize_data['order_number'],
                        'date': serialize_data['order_date'],
                        'file': order_file
                    },
                )
            else:
                create_data['program_order_id'] = None
        else:
            update_program_data = {
                'number': serialize_data['order_number'],
                'date': serialize_data['order_date']
            }
            if 'order_file' in serialize_data.keys() and \
                    serialize_data.get('order_file') not in [None, 'null']:
                update_program_data['file'] = order_file
            program_order_service.update_program_order(
                serialize_data['order_id'],
                update_program_data
            )
            create_data['program_order_id'] = serialize_data['order_id']

        # Добавляем или обновляем ДПП
        if not create:
            program_orm.update_record({'object_id': serialize_data.get('object_id')}, create_data)
            program_id = serialize_data.get('object_id')
        else:
            program_id = uuid.uuid4()
            program_orm.create_record({**create_data, 'object_id': program_id})

        # Устанавливаем категории для обработанной ДПП
        program_orm.clear_many_to_many({'object_id': program_id}, 'categories')
        program_orm.add_many_to_many({'object_id': program_id}, 'categories', categories)


program_service = ProgramService()
