import os

from apps.commons.utils.django.exception import ExceptionHandling
from apps.docs.opertaions.base_doc import BaseDocOperation
from apps.docs.selectors.program_order import program_order_orm


class DeleteProgramOrderOperation(BaseDocOperation):
    """Удаление приказа ДПП"""

    def action(self, process_data: dict):
        """Действие удаления"""
        try:
            if 'object_id' in process_data['process_data']['document_data'].keys():
                doc = program_order_orm.get_one_record_or_none(
                    filter_by={'object_id': process_data['process_data']['document_data']['object_id']}
                )
                if doc.file:
                    os.remove(doc.file.path)
                program_order_orm.delete_record(filter_by={'object_id': doc.object_id})
                self.process_completed = True
                self.success_message = 'Документ успешно удален'
                self._doc_operation_success()
        except Exception:
            self.error_message = ExceptionHandling.get_traceback()
            self._doc_operation_error()
            self.process_completed = False
