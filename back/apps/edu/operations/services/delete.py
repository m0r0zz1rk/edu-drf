from typing import Union

from django.apps import apps

from apps.commons.abc.main_processing import MainProcessing
from apps.commons.utils.django.exception import ExceptionHandling
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS

education_service_model = apps.get_model('edu', 'EducationService')
information_service_model = apps.get_model('edu', 'InformationService')


class DeleteService(MainProcessing):
    """Удаление услуги (курса, мероприятия)"""

    def __init__(self, income_data: dict, service_type: str, request=None):
        """
        Инициализация класса - установка типа услуги и необходимых ключей для модели
        :param service_type: Тип услуги
        """
        self.service_type = service_type
        super(DeleteService, self).__init__(income_data, request)

    def _validate_process_data(self) -> Union[bool, str]:
        """
        Валидация данных для удаления услуги
        :return: true - данные валидны, false - данные не валидны, str - traceback
        """
        try:
            if 'object_id' not in self.process_data.keys():
                return False
            return True
        except:
            return ExceptionHandling.get_traceback()

    def _main_process(self):
        """Удаление услуги"""
        try:
            service_model = information_service_model
            if self.service_type == 'edu':
                service_model = education_service_model
            service_model.objects.filter(object_id=self.process_data['object_id']).first().delete()
            self.process_completed = True
        except Exception as e:
            description = 'информационно-консультационной услуги (мероприятия)'
            if self.service_type == 'edu':
                description = 'образовательной услуги (курса)'
            self.ju.create_journal_rec(
                {
                    'source': self.source,
                    'module': self.module,
                    'status': ERROR,
                    'description': f'Системная ошибка в процессе удаления {description}'
                },
                repr(self.process_data),
                ExceptionHandling.get_traceback()
            )
            self.process_completed = False

    def _process_success(self):
        """Фиксация сообщения об успешном удалении услуги в журнале"""
        description = 'Информационно-консультационная услуга (мероприятие)'
        if self.service_type == 'edu':
            description = 'Образовательная услуга (курс)'
        self.ju.create_journal_rec(
            {
                'source': self.source,
                'module': self.module,
                'status': SUCCESS,
                'description': f'{description} успешно удалена'
            },
            repr(self.process_data),
            None
        )
