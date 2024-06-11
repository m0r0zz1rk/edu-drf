from typing import Union

from django.apps import apps

from apps.commons.abc.main_processing import MainProcessing
from apps.commons.utils.django.exception import ExceptionHandling
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS

education_service_model = apps.get_model('edu', 'EducationService')


class AddUpdateEducationService(MainProcessing):
    """Добавление/обновление образовательной услуги (курса)"""
    education_service_required_keys = [
        *[f.name for f in education_service_model._meta.get_fields() if f.name not in ['date_create', 'program_id']],
        'program'
    ]

    def _validate_process_data(self) -> Union[bool, str]:
        """
        Валидация данных для добавления/обновления образовательной услуги (курса)
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
        """Добавление/обновление образовательной услуги (курса)"""
        try:
            self.process_data['program_id'] = self.process_data['program']
            del self.process_data['program']
            education_service_model.objects.update_or_create(
                object_id=self.process_data['object_id'],
                defaults=self.process_data
            )
            self.process_completed = True
        except Exception as e:
            self.ju.create_journal_rec(
                {
                    'source': self.source,
                    'module': self.module,
                    'status': ERROR,
                    'description': 'Ошибка в процессе добавлении/удалении образовательной услуги (курса)'
                },
                repr(self.process_data),
                ExceptionHandling.get_traceback()
            )
            self.process_completed = False

    def _process_success(self):
        """Фиксация сообщения об успешном добавлении/обновлении элемента КУГ в журнале"""
        self.ju.create_journal_rec(
            {
                'source': self.source,
                'module': self.module,
                'status': SUCCESS,
                'description': 'Образовательная услуга (курс) успешно добавлена/обновлена'
            },
            repr(self.process_data),
            None
        )
