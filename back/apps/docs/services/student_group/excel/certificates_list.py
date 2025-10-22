import os
import uuid

from xlsxtpl.writerx import BookWriter

from apps.applications.consts.education import STUDENT
from apps.applications.selectors.course_certificate import course_certificate_orm
from apps.commons.utils.data_types.date import date_utils
from apps.commons.utils.django.settings import settings_utils
from apps.docs.services.student_group.base_student_group_doc import BaseStudentGroupDoc
from apps.edu.selectors.student_group import student_group_orm


class CertificatesList(BaseStudentGroupDoc):
    """
    Класс для генерации ведомости удостоверений учебной группы
    """

    def __init__(self, group_id: uuid, orders_info: dict):
        """
        Инициализация класса - установка учебной группы и информации по приказам о зачислении
        и отчислении
        :param group_id: object_id учебной группы
        :param orders_info: словарь номерами и датами приказов о зачислении и отчислении
        """
        super().__init__(group_id)
        self.orders_info = orders_info

    def _get_context(self) -> dict:
        pass

    def _save_order_data(self):
        """
        Сохранение информации о приказах об зачислении и отчислении в учебную группу
        :return:
        """
        student_group_orm.update_record(
            dict(object_id=self.student_group.object_id),
            self.orders_info
        )

    def _get_student_info(self) -> list:
        """
        Получение информации по обучающимся и их удостоверениям
        :return: список с информацией по обучающимся
        """
        result = []
        apps = self._get_group_applications()
        for index, app in enumerate(apps, start=1):
            student = {
                'id': index,
                'surname': app.profile.surname,
                'name': app.profile.name,
                'patronymic': app.profile.patronymic,
                'registration_number': '',
                'blank_serial': '',
                'blank_number': '',
                'note': '' if app.education_level != STUDENT else 'Справка'
            }
            certificate_info = course_certificate_orm.get_one_record_or_none(
                dict(application_id=app.object_id)
            )
            if certificate_info:
                student['registration_number'] = certificate_info.registration_number
                student['blank_serial'] = certificate_info.blank_serial
                student['blank_number'] = certificate_info.blank_number
            result.append(student)
        return result

    def _fill_page(self, writer: BookWriter):
        """
        Заполнение данных о курсе и сертификатов обучающихся на лист книги Excel
        :param writer: объект BookWriter для записи данных в шаблон Excel
        :return:
        """
        self._save_order_data()
        dep, manager = self._get_department_and_manager()
        date_start, date_end = self._get_date_start_and_end()
        _, program_type = self._get_program_and_certificates_types()
        info = {
            'dep': dep,
            'type_dpp': program_type,
            'name_dpp': self.student_group.ou.program.name,
            'duration': self.student_group.ou.program.duration,
            'code': self.student_group.code,
            'manager': manager,
            'day_start': date_start.strftime('%d'),
            'month_start': date_utils.get_month_genitive_case(date_start.strftime('%B')),
            'year_start': date_start.strftime('%Y'), 'day_finish': date_end.strftime('%d'),
            'month_finish': date_utils.get_month_genitive_case(date_end.strftime('%B')),
            'year_finish': date_end.strftime('%Y'), 'date_get': date_end.strftime('%d.%m.%Y'),
            'date_enroll': self.orders_info.get('date_enroll').strftime('%d.%m.%Y'),
            'date_exp': self.orders_info.get('date_exp').strftime('%d.%m.%Y'),
            'number_enroll': self.orders_info.get('enroll_number'),
            'number_exp': self.orders_info.get('exp_number'),
            'students': self._get_student_info()
        }
        writer.render_sheet(info, 'Ведомость выдачи удостоверений', 0)

    def _generate_wb(self):
        """
        Запись данных в книгу Excel
        :return:
        """
        # writer = BookWriter(self._get_template_path(('Ведомость удостоверений',)))
        writer = BookWriter(os.path.join(
            settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
            'Шаблоны',
            'Ведомость удостоверений',
            'шаблон_ОУ.xlsx'
        ))
        self._fill_page(writer)
        return writer
