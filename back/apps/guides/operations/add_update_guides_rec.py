from apps.commons.processes.db.add_update_database_record import AddUpdateDataBaseRecord
from apps.guides.operations.base_operation_guide import BaseOperationGuide


class AddUpdateGuidesRec(BaseOperationGuide):
    """Добавление/обновление записи в справочник"""

    def action(self, process_data):
        proc = AddUpdateDataBaseRecord(process_data)
        return proc.process_completed
