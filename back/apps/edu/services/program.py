import uuid
from typing import Optional

from apps.authen.services.profile import ProfileService
from apps.commons.services.ad.ad_centre import AdCentreService
from apps.edu.operations.program.add_update_program import AddUpdateProgramOperation
from apps.edu.selectors.program import program_model


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
        except:
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
        try:
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
                cats += cat.name+','
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
        except:
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
        except Exception:
            return None

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
