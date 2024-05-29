import uuid
from typing import Optional

from django.apps import apps

from apps.commons.utils.ad.ad_centre import AdCentreUtils
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.request import RequestUtils
from apps.docs.opertaions.program_order.add_program_order_operation import AddUpdateProgramOrderOperation
from apps.guides.utils.audience_category import AudienceCategoryUtils
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.utils.journal_utils import JournalUtils

program_model = apps.get_model('edu', 'Program')


class AddUpdateProgramOperation:
    """Класс действия для добавления/обновления ДПП"""

    ju = JournalUtils()
    acu = AudienceCategoryUtils()
    adcu = AdCentreUtils()
    ru = RequestUtils()

    program_data = process_completed = error = None
    source = 'Добавление/обновление ДПП'
    program_fields = [
        *[f.name for f in program_model._meta.get_fields()
          if f.name not in ['date_create', 'program_order']],
        'order_id',
        'order_number',
        'order_date',
        'order_file'
    ]

    def __init__(self, program_data: dict, request=None):
        """
        Инициализация класса
        :param program_data: словарь с данными о ДПП
        :param request: Объект request
        """
        if request:
            self.source = self.ru.get_source_display_name(request)
        self.program_data = program_data
        if not self._validate_program_data():
            self._program_operation_error('Данные не прошли валидацию')
        else:
            self._main_action()

    def _program_operation_error(self, traceback: str):
        """
        Фиксация ошибки при выполнении действия над ДПП
        :param traceback: traceback возникшей в процессе ошибки
        :return:
        """
        self.ju.create_journal_rec(
            {
                'source': self.source,
                'module': EDU,
                'status': ERROR,
                'description': 'Произошла ошибка в процессе добавления/обновления ДПП'
            },
            repr(self.program_data),
            traceback
        )

    def _program_operation_success(self):
        """
        Фиксация сообщения об успешном выполнении действия над ДПП
        :return:
        """
        self.ju.create_journal_rec(
            {
                'source': self.source,
                'module': EDU,
                'status': SUCCESS,
                'description': 'ДПП успешно добавлено/обновлено'
            },
            repr(self.program_data),
            None
        )

    def _validate_program_data(self) -> bool:
        """Валидация полей данных о ДПП"""
        for field in self.program_fields:
            if field not in ['object_id', 'date_create', 'program', 'order_file']:
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
                cat_list = self.program_data['categories'].split(',')
                cat_obj_list = [
                    self.acu.get_category_object_by_name(cat_name).object_id
                    for cat_name in cat_list
                    if self.acu.get_category_object_by_name(cat_name) is not None
                ]
                del self.program_data['categories']
            if self.program_data['order_id'] in [None, 'null']:
                add_order_proc = self._add_program_order()
                if add_order_proc is None:
                    return False
                del self.program_data['order_number']
                del self.program_data['order_date']
                if 'order_file' in self.program_data.keys():
                    del self.program_data['order_file']
                self.program_data['program_order_id'] = add_order_proc
            else:
                update_order_proc = self._update_program_order()
                if update_order_proc is None:
                    return False
                del self.program_data['order_number']
                del self.program_data['order_date']
                if 'order_file' in self.program_data.keys():
                    del self.program_data['order_file']
                self.program_data['program_order_id'] = self.program_data['order_id']
            del self.program_data['order_id']
            if self.program_data['object_id'] not in [None, 'null']:
                object_id = self.program_data['object_id']
                del self.program_data['object_id']
                dpp, _ = program_model.objects.update_or_create(
                    object_id=object_id,
                    defaults=self.program_data
                )
            else:
                del self.program_data['object_id']
                dpp, _ = program_model.objects.update_or_create(
                    **self.program_data
                )
            dpp.categories.clear()
            dpp.categories.add(*cat_obj_list)
            self._program_operation_success()
            self.process_completed = True
        except Exception:
            self.process_completed = False
            self._program_operation_error(ExceptionHandling.get_traceback())
