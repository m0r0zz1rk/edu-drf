from apps.commons.processes.db.delete_database_record import DeleteDataBaseRecord
from apps.guides.operations.base_operation_guide import BaseOperationGuide


class DeleteGuidesRec(BaseOperationGuide):
    """Удаление записи из справочника"""

    def action(self, process_data):
        proc = DeleteDataBaseRecord(process_data)
        self.process_completed = proc.process_completed
