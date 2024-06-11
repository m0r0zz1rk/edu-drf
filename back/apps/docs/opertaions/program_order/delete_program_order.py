import os

from django.apps import apps

from apps.commons.utils.django.exception import ExceptionHandling
from apps.docs.opertaions.base_doc import BaseDocOperation

program_order_model = apps.get_model('docs', 'ProgramOrder')


class DeleteProgramOrderOperation(BaseDocOperation):
    """Удаление приказа ДПП"""

    def action(self, process_data: dict):
        """Действие удаления"""
        try:
            if 'object_id' in process_data['process_data']['document_data'].keys():
                order = program_order_model.objects.get(
                    object_id=process_data['process_data']['document_data']['object_id']
                )
                if order.file:
                    os.remove(order.file.path)
                order.delete()
                self.process_completed = True
                self.success_message = 'Документ успешно удален'
                self._doc_operation_success()
        except Exception:
            self.error_message = ExceptionHandling.get_traceback()
            self._doc_operation_error()
            self.process_completed = False