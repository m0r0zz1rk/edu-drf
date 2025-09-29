from typing import Union

from apps.commons.abc.main_processing import MainProcessing
from apps.commons.services.ad.ad_centre import AdCentreService
from apps.commons.utils.django.exception import ExceptionHandling
from apps.edu.selectors.services.education_service import education_service_model, education_service_orm
from apps.edu.selectors.services.information_service import information_service_model, information_service_orm
from apps.guides.services.audience_category import AudienceCategoryService
from apps.guides.services.event_type import EventTypeService
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.services.journal import journal_service


class AddUpdateService(MainProcessing):
    """Добавление/обновление услуги (курса, мероприятия)"""
    acs = AudienceCategoryService()
    ets = EventTypeService()
    ads = AdCentreService()

    service_required_keys = []
    service_type = None

    def __init__(self, income_data: dict, service_type: str, request=None):
        """
        Инициализация класса - установка типа услуги и необходимых ключей для модели
        :param service_type: Тип услуги
        """
        self.service_type = service_type
        if self.service_type == 'edu':
            self.service_required_keys = [
                *[f.name for f in education_service_model._meta.concrete_fields
                  if f.name not in ['date_create', 'program_id']],
                'program'
            ]
        else:
            self.service_required_keys = [
                f.name for f in information_service_model._meta.concrete_fields
                if f.name != 'date_create'
            ]
        super(AddUpdateService, self).__init__(income_data, request)

    def _validate_process_data(self) -> Union[bool, str]:
        """
        Валидация данных для добавления/обновления услуги
        :return: true - данные валидны, false - данные не валидны, str - traceback
        """
        try:
            for key in self.service_required_keys:
                if key not in self.process_data.keys():
                    return False
            return True
        except Exception:
            return ExceptionHandling.get_traceback()

    def _main_process(self):
        """Добавление/обновление услуги"""
        try:
            cat_obj_list = []
            service_orm = information_service_orm
            if self.service_type == 'edu':
                self.process_data['program_id'] = self.process_data['program']
                del self.process_data['program']
                service_orm = education_service_orm
            else:
                event_type = self.ets.get_event_type_object_by_name(self.process_data['type'])
                self.process_data['type_id'] = event_type.object_id
                del self.process_data['type']
                department = self.ads.get_ad_centre('display_name', self.process_data['department'])
                self.process_data['department_id'] = department.object_id
                del self.process_data['department']
                if len(self.process_data['categories']) > 0:
                    cat_list = self.process_data['categories'].split(';;')
                    cat_obj_list = [
                        self.acs.get_category_object_by_name(cat_name).object_id
                        for cat_name in cat_list
                        if self.acs.get_category_object_by_name(cat_name) is not None
                    ]
                    del self.process_data['categories']
            service = service_orm.get_one_record_or_none(filter_by={'object_id': self.process_data['object_id']})
            if service:
                service_orm.update_record(
                    filter_by={'object_id': self.process_data['object_id']},
                    update_object=self.process_data
                )
            else:
                service = service_orm.create_record(self.process_data)
            if self.service_type == 'info':
                service.categories.clear()
                service.categories.add(*cat_obj_list)
            self.process_completed = True
        except Exception:
            description = 'информационно-консультационной услуги (мероприятия)'
            if self.service_type == 'edu':
                description = 'образовательной услуги (курса)'
            journal_service.create_journal_rec(
                {
                    'source': self.source,
                    'module': self.module,
                    'status': ERROR,
                    'description': f'Ошибка в процессе добавления/обновления {description}'
                },
                repr(self.process_data),
                ExceptionHandling.get_traceback()
            )
            self.process_completed = False

    def _process_success(self):
        """Фиксация сообщения об успешном добавлении/обновлении услуги в журнале"""
        description = 'Информационно-консультационная услуга (мероприятие)'
        if self.service_type == 'edu':
            description = 'Образовательная услуга (курс)'
        journal_service.create_journal_rec(
            {
                'source': self.source,
                'module': self.module,
                'status': SUCCESS,
                'description': f'{description} успешно добавлена/обновлена'
            },
            repr(self.process_data),
            None
        )
