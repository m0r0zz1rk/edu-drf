from typing import Union

from apps.commons.abc.main_processing import MainProcessing
from apps.commons.utils.django.exception import ExceptionHandling
from apps.edu.selectors.student_group import student_group_model
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS


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
        except:
            return ExceptionHandling.get_traceback()

    def _main_process(self):
        """Удаление учебной группы"""
        try:
            student_group_model.objects.filter(object_id=self.process_data['group_id']).first().delete()
            self.process_completed = True
        except Exception as e:
            self.ju.create_journal_rec(
                {
                    'source': self.source,
                    'module': self.module,
                    'status': ERROR,
                    'description': f'Системная ошибка в процессе удаления учебной группы'
                },
                repr(self.process_data),
                ExceptionHandling.get_traceback()
            )
            self.process_completed = False

    def _process_success(self):
        """Фиксация сообщения об успешном удалении учебной группы"""
        self.ju.create_journal_rec(
            {
                'source': self.source,
                'module': self.module,
                'status': SUCCESS,
                'description': f'Учебная группа успешно удалена'
            },
            repr(self.process_data),
            None
        )