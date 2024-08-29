import uuid

from django.apps import apps
from django.core.files import File

from apps.commons.utils.django.exception import ExceptionHandling
from apps.docs.opertaions.base_doc import BaseDocOperation

program_order_model = apps.get_model('docs', 'ProgramOrder')


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
                if 'file' in doc_data.keys() and type(doc_data['file']) is str:
                    path = doc_data['file']
                    del doc_data['file']
                    doc, _ = program_order_model.objects.update_or_create(
                        object_id=uuid.uuid4(),
                        **doc_data
                    )
                    doc.file = File(open(path, 'rb'))
                    doc.save()
                else:
                    doc, _ = program_order_model.objects.update_or_create(
                        object_id=object_id,
                        defaults=doc_data
                    )
            else:
                if type(doc_data['file']) is str:
                    path = doc_data['file']
                    del doc_data['file']
                    doc, _ = program_order_model.objects.update_or_create(
                        object_id=uuid.uuid4(),
                        **doc_data
                    )
                    doc.file = File(open(path, 'rb'))
                    doc.save()
                else:
                    doc, _ = program_order_model.objects.update_or_create(
                        object_id=uuid.uuid4(),
                        **doc_data
                    )
            self.doc_id = doc.object_id
            self.process_completed = True
            self.success_message = 'Приказ ДПП успешно добавлен/обновлен'
            self._doc_operation_success()
        except Exception:
            self.error_message = ExceptionHandling.get_traceback()
            self._doc_operation_error()
            self.process_completed = False
