from typing import Union

from django.apps import apps

from apps.commons.abc.main_processing import MainProcessing
from apps.commons.utils.django.exception import ExceptionHandling
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS

education_service_model = apps.get_model('edu', 'EducationService')


class DeleteEducationService(MainProcessing):
    """Удаление образовательной услуги (курса)"""
    education_service_required_keys = [
        'object_id',
    ]

    def _validate_process_data(self) -> Union[bool, str]:
        """
        Валидация данных для удаления элемента КУГ
        :return: true - данные валидны, false - данные не валидны, str - traceback
        """
        try:
            for key in self.education_service_required_keys:
                if key not in self.process_data.keys():
                    return False
            return True
        except:
            return ExceptionHandling.get_traceback()

    def _main_process(self):
        """Удаление элемента КУГ"""
        try:
            education_service_model.objects.filter(object_id=self.process_data['object_id']).first().delete()
            self.process_completed = True
        except Exception as e:
            self.ju.create_journal_rec(
                {
                    'source': self.source,
                    'module': self.module,
                    'status': ERROR,
                    'description': 'Системная ошибка в процессе удаления образовательной услуги'
                },
                repr(self.process_data),
                ExceptionHandling.get_traceback()
            )
            self.process_completed = False

    def _process_success(self):
        """Фиксация сообщения об успешном удалении элемента КУГ в журнале"""
        self.ju.create_journal_rec(
            {
                'source': self.source,
                'module': self.module,
                'status': SUCCESS,
                'description': 'Образовательная услуга (курс) успешно удалена'
            },
            repr(self.process_data),
            None
        )
