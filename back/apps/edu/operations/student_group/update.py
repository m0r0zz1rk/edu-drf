from typing import Union

from apps.commons.abc.main_processing import MainProcessing
from apps.commons.utils.django.exception import ExceptionHandling
from apps.edu.selectors.student_group import student_group_orm
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.services.journal import journal_service


class UpdateStudentGroup(MainProcessing):
    """Обновление учебной группы"""
    required_keys = ['group_id', 'code', 'curator_id', 'status', 'form', 'plan_seats_number']

    def _validate_process_data(self) -> Union[bool, str]:
        """
        Валидация данных при обновлении учебной группы
        :return: true - данные валидны, false - данные не валидны, str - traceback
        """
        try:
            for key in self.required_keys:
                if key not in self.process_data.keys():
                    return False
            return True
        except Exception:
            return ExceptionHandling.get_traceback()

    def _main_process(self):
        """Обновление учебной группы"""
        try:
            group_id = self.process_data['group_id']
            del self.process_data['group_id']
            student_group_orm.update_record(
                filter_by={'object_id': group_id},
                update_object=self.process_data
            )
            self.process_completed = True
        except Exception:
            journal_service.create_journal_rec(
                {
                    'source': self.source,
                    'module': self.module,
                    'status': ERROR,
                    'description': 'Ошибка в процессе обновления учебной группы'
                },
                repr(self.process_data),
                ExceptionHandling.get_traceback()
            )
            self.process_completed = False

    def _process_success(self):
        """Фиксация сообщения об успешном обновлении учебной группы"""
        journal_service.create_journal_rec(
            {
                'source': self.source,
                'module': self.module,
                'status': SUCCESS,
                'description': 'Учебная группа успешно обновлена'
            },
            repr(self.process_data),
            None
        )
