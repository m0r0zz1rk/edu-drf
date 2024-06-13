import uuid
from typing import Optional

from django.apps import apps

from apps.commons.services.ad.ad_centre import AdCentreService
from apps.commons.utils.django.exception import ExceptionHandling
from apps.docs.opertaions.program_order.add_program_order import AddUpdateProgramOrderOperation
from apps.edu.operations.program.base_program import BaseProgramOperation
from apps.guides.services.audience_category import AudienceCategoryService

program_model = apps.get_model('edu', 'Program')


class AddUpdateProgramOperation(BaseProgramOperation):
    """Класс действия для добавления/обновления ДПП"""

    acu = AudienceCategoryService()
    adcu = AdCentreService()

    error_description = 'Произошла ошибка в процессе добавления/обновления ДПП'
    success_description = 'ДПП успешно добавлено/обновлено'
    program_fields = [
        *[f.name for f in program_model._meta.get_fields()
          if f.name not in ['date_create', 'calendarchartchapter', 'educationservice', 'program_order']],
        'order_id',
        'order_number',
        'order_date',
        'order_file'
    ]
    dpp = None

    def _validate_program_data(self) -> bool:
        """Валидация полей данных о ДПП"""
        for field in self.program_fields:
            if field not in ['date_create', 'kug_edit', 'program', 'order_file']:
                if field not in self.program_data.keys():
                    return False
        return True

    def _add_program_order(self) -> Optional[uuid.uuid4]:
        """
        Добавление приказа ДПП
        :return: None - ошибка при добавлении приказа ДПП
        """
        proc = AddUpdateProgramOrderOperation(
            {
                'number': self.program_data['order_number'],
                'date': self.program_data['order_date'],
                'file': self.program_data['order_file']
            },
            'ProgramOrder',
            None
        )
        if not proc.process_completed:
            self._program_operation_error(proc.error_message)
            return False
        return proc.doc_id

    def _update_program_order(self) -> bool:
        """
        Обновление приказа ДПП
        :return: True - успешно, False - ошибка
        """
        doc_data = {
                'object_id': self.program_data['order_id'],
                'number': self.program_data['order_number'],
                'date': self.program_data['order_date']
        }
        if 'order_file' in self.program_data.keys() and \
                self.program_data['order_file'] not in [None, 'null']:
            doc_data['file'] = self.program_data['order_file']
        proc = AddUpdateProgramOrderOperation(
            doc_data,
            'ProgramOrder',
            None
        )
        if not proc.process_completed:
            self._program_operation_error(proc.error_message)
            return False
        return True

    def _main_action(self):
        try:
            self.program_data['department'] = self.adcu.get_ad_centre(
                'display_name',
                self.program_data['department']
            )
            cat_obj_list = []
            if len(self.program_data['categories']) > 0:
                cat_list = self.program_data['categories'].split(';;')
                cat_obj_list = [
                    self.acu.get_category_object_by_name(cat_name).object_id
                    for cat_name in cat_list
                    if self.acu.get_category_object_by_name(cat_name) is not None
                ]
                del self.program_data['categories']
            if self.program_data['order_id'] in [None, 'null']:
                if self.program_data['order_number'] is not None:
                    add_order_proc = self._add_program_order()
                    if add_order_proc is None:
                        return False
                    self.program_data['program_order_id'] = add_order_proc
                else:
                    self.program_data['program_order_id'] = None
            else:
                update_order_proc = self._update_program_order()
                if update_order_proc is None:
                    return False
                self.program_data['program_order_id'] = self.program_data['order_id']
            del self.program_data['order_number']
            del self.program_data['order_date']
            del self.program_data['order_file']
            del self.program_data['order_id']
            if self.program_data['object_id'] not in [None, 'null']:
                object_id = self.program_data['object_id']
                del self.program_data['object_id']
                self.dpp, _ = program_model.objects.update_or_create(
                    object_id=object_id,
                    defaults=self.program_data
                )
            else:
                del self.program_data['object_id']
                self.dpp, _ = program_model.objects.update_or_create(
                    object_id=uuid.uuid4(),
                    **self.program_data
                )
            self.dpp.categories.clear()
            self.dpp.categories.add(*cat_obj_list)
            self.success_description = 'ДПП успешно добавлена/обновлена'
            self._program_operation_success()
            self.process_completed = True
        except Exception:
            self.process_completed = False
            self.error_description = 'Произошила ошибка при удалении/обновлении ДПП'
            self._program_operation_error(ExceptionHandling.get_traceback())
