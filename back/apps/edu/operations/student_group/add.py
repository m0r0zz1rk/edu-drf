from typing import Union

from apps.commons.abc.main_processing import MainProcessing
from apps.commons.utils.django.exception import ExceptionHandling
from apps.edu.exceptions.student_group.generate_code_error import GenerateCodeError
from apps.edu.selectors.student_group import student_group_orm
from apps.edu.services.service.education_service import EducationServiceService
from apps.edu.services.service.information_service import InformationServiceService
from apps.edu.services.student_group import StudentGroupService
from apps.journal.consts.journal_rec_statuses import ERROR, SUCCESS
from apps.journal.services.journal import journal_service


class AddStudentGroup(MainProcessing):
    """Добавление учебной группы"""
    sgs = StudentGroupService()
    ess = EducationServiceService()
    iss = InformationServiceService()

    required_keys = ['type', 'service_id', 'plan_seats_number']

    def _validate_process_data(self) -> Union[bool, str]:
        """
        Валидация данных для добавления учебной группы
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
        """Добавление учебной группы"""
        try:
            department = ''
            if self.process_data['type'] == 'ou':
                self.process_data['ou_id'] = self.process_data['service_id']
                dep = self.ess.get_info_by_service(
                    'object_id',
                    self.process_data['service_id'],
                    'dep_name'
                )
            else:
                self.process_data['iku_id'] = self.process_data['service_id']
                dep = self.iss.get_info_by_service(
                    'object_id',
                    self.process_data['service_id'],
                    'dep_name'
                )
            if dep is not None:
                department = dep
            self.process_data['code'] = self.sgs.generate_group_code(
                department,
                self.process_data['service_id'],
                self.process_data['type']
            )
            del self.process_data['service_id']
            del self.process_data['type']
            student_group_orm.create_record(self.process_data)
            self.process_completed = True
        except GenerateCodeError:
            journal_service.create_journal_rec(
                {
                    'source': self.source,
                    'module': self.module,
                    'status': ERROR,
                    'description': 'Ошибка в процессе генерации кода учебной группы'
                },
                repr(self.process_data),
                ExceptionHandling.get_traceback()
            )
            self.process_completed = False
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': self.source,
                    'module': self.module,
                    'status': ERROR,
                    'description': 'Ошибка в процессе добавления учебной группы'
                },
                repr(self.process_data),
                ExceptionHandling.get_traceback()
            )
            self.process_completed = False

    def _process_success(self):
        """Фиксация сообщения об успешном добавлении учебной группы"""
        journal_service.create_journal_rec(
            {
                'source': self.source,
                'module': self.module,
                'status': SUCCESS,
                'description': 'Учебная группа успешно добавлена'
            },
            repr(self.process_data),
            None
        )
