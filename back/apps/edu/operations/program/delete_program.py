from django.apps import apps

from apps.commons.utils.django.exception import ExceptionHandling
from apps.docs.opertaions.program_order.delete_program_order import DeleteProgramOrderOperation
from apps.edu.operations.program.base_program import BaseProgramOperation

program_model = apps.get_model('edu', 'Program')


class DeleteProgramOperation(BaseProgramOperation):
    """Класс для удаления ДПП"""

    def _validate_program_data(self) -> bool:
        if 'object_id' in self.program_data.keys():
            return True
        return False

    def _main_action(self):
        try:
            dpp = program_model.objects.get(object_id=self.program_data['object_id'])
            if dpp.program_order:
                DeleteProgramOrderOperation(
                    {
                        'object_id': dpp.program_order.object_id,
                    },
                    'ProgramOrder',
                    None
                )
            dpp.delete()
            self.success_description = 'ДПП успешно удалена'
            self._program_operation_success()
            self.process_completed = True
        except Exception:
            self.process_completed = False
            self.error_description = 'Произошла ошибка при удалении ДПП'
            self._program_operation_error(ExceptionHandling.get_traceback())
