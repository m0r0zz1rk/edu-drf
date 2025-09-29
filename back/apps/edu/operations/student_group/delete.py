from typing import Union

from apps.commons.abc.main_processing import MainProcessing
from apps.commons.utils.django.exception import ExceptionHandling
from apps.edu.selectors.student_group import student_group_orm
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.services.journal import journal_service


class DeleteStudentGroup(MainProcessing):
    """Удаление учебной группы"""

    def _validate_process_data(self) -> Union[bool, str]:
        """
        Валидация данных для удаления услуги
        :return: true - данные валидны, false - данные не валидны, str - traceback
        """
        try:
            if 'group_id' not in self.process_data.keys():
                return False
            return True
        except Exception:
            return ExceptionHandling.get_traceback()

    def _main_process(self):
        """Удаление учебной группы"""
        try:
            student_group_orm.delete_record(filter_by={'object_id': self.process_data['group_id']})
            self.process_completed = True
        except Exception:
            journal_service.create_journal_rec(
                {
                    'source': self.source,
                    'module': self.module,
                    'status': ERROR,
                    'description': 'Системная ошибка в процессе удаления учебной группы'
                },
                repr(self.process_data),
                ExceptionHandling.get_traceback()
            )
            self.process_completed = False

    def _process_success(self):
        """Фиксация сообщения об успешном удалении учебной группы"""
        journal_service.create_journal_rec(
            {
                'source': self.source,
                'module': self.module,
                'status': SUCCESS,
                'description': 'Учебная группа успешно удалена'
            },
            repr(self.process_data),
            None
        )
