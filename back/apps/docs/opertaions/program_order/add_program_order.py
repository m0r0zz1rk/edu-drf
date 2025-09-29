import uuid

from django.core.files import File

from apps.commons.utils.django.exception import ExceptionHandling
from apps.docs.opertaions.base_doc import BaseDocOperation
from apps.docs.selectors.program_order import program_order_orm


class AddUpdateProgramOrderOperation(BaseDocOperation):
    """Добавление/Обновление приказа ДПП"""

    required_fields = [
        'number',
        'date',
    ]

    def action(self, process_data: dict):
        """Процесс добавления/обновления приказа ДПП"""
        try:
            doc_data = process_data['process_data']['document_data']
            for field in self.required_fields:
                if field not in doc_data.keys():
                    self.error = f'Не найдено поле "{field}" в полученных данных'
                    self.error = True
                    self.process_completed = False
                    return False
            if 'object_id' in doc_data.keys():
                object_id = doc_data['object_id']
                del doc_data['object_id']
                path = None
                if 'file' in doc_data.keys() and type(doc_data['file']) is str:
                    path = doc_data['file']
                    del doc_data['file']
                program_order_orm.update_record(filter_by={'object_id': object_id}, update_object=doc_data)
                doc = program_order_orm.get_one_record_or_none(filter_by={'object_id': object_id})
                if doc and path:
                    program_order_orm.update_record(
                        filter_by={'object_id': doc.object_id},
                        update_object={'file': File(open(path, 'rb')), 'updated_from_new': True}
                    )
            else:
                path = None
                if type(doc_data['file']) is str:
                    path = doc_data['file']
                    del doc_data['file']
                doc = program_order_orm.create_record(doc_data)
                if path:
                    program_order_orm.update_record(
                        filter_by={'object_id': doc.object_id},
                        update_object={'file': File(open(path, 'rb')), 'updated_from_new': True}
                    )
            self.doc_id = doc.object_id
            self.process_completed = True
            self.success_message = 'Приказ ДПП успешно добавлен/обновлен'
            self._doc_operation_success()
        except Exception:
            self.error_message = ExceptionHandling.get_traceback()
            self._doc_operation_error()
            self.process_completed = False
