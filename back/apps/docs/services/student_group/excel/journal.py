import os
import re
import uuid

from xlsxtpl.writerx import BookWriter

from apps.commons.utils.django.settings import settings_utils
from apps.docs.services.student_group.base_student_group_doc import BaseStudentGroupDoc
from apps.edu.exceptions.student_group.lessons_not_found import LessonsNotFound, LessonsWithControlNotFound
from apps.edu.serializers.schedule import date_utils
from apps.edu.services.schedule import ScheduleService

_base_student_attributes = ['surname', 'name', 'patronymic', 'oo', 'pos']

_course_student_attributes = [
    *_base_student_attributes,
    'region',
    'mo',
    'pos_cat',
    'age',
    'birthday',
    'sex',
    'snils',
    'edu_level',
    'diploma_surname',
    'edu_serial',
    'edu_number',
    'type_pay',
    'reg_number',
    'serial_blank',
    'number_blank'
]

_event_student_attributes = [*_base_student_attributes, 'terr']


class JournalDoc(BaseStudentGroupDoc):
    """
    Класс для формирования журнала по учебной группе
    """

    _lessons = None

    class StudentCourseInfo:
        """
        Класс информации для студента на ОУ
        """
        def __init__(self, **info):
            """
            Инициализация класса - подстановка значений
            :param info: словарь
            """
            for attribute in _course_student_attributes:
                setattr(self, attribute, info.get(attribute, '-'))

    class StudentEventInfo:
        """
        Класс информации для студента на ИКУ
        """

        def __init__(self, **info):
            """
            Инициализация класса - подстановка значений
            :param info: словарь
            """
            for attribute in _event_student_attributes:
                setattr(self, attribute, info.get(attribute, '-'))

    def __init__(self, group_id: uuid):
        """
        Инициализация класса - получение группы, проверка на наличие занятий в расписании
        и наличие занятий с формой проверки
        :param group_id: object_id учебной группы
        """
        super().__init__(group_id)
        schedule_service = ScheduleService(group_id)
        self._lessons = schedule_service.get_group_lessons()
        if self._lessons.count() == 0:
            raise LessonsNotFound
        if not self._lessons.exclude(control='').exists():
            raise LessonsWithControlNotFound

    def _get_department_short_name(self) -> str:
        """
        Получение сокращения названия подразделения
        :return: Сокращение названия центра
        """
        if self.student_group.ou:
            department = self.student_group.ou.program.department
        else:
            department = self.student_group.iku.department
        dep_name_split = re.split(' |-', department)
        short_dep = ''
        for word in dep_name_split:
            short_dep += word[:1].upper()
        return short_dep

    def _get_categories(self) -> str:
        """
        Получение строки, содержащей список категорий слушателей учебной группы
        :return: строка
        """
        if self.student_group.ou:
            categories = self.student_group.ou.program.categories.all()
        else:
            categories = self.student_group.iku.categories.all()
        categories_str = ''
        for category in categories:
            categories_str += f'{category.name} '
        return categories_str[:-1]

    def _get_lessons_count_by_type(self) -> dict:
        """
        Получение словаря с количеством часов по типам занятий:
        всего часов, лекций, практик, стажировок, сам. работы
        :return: словарь с пятью ключами
        """
        hours = {
            'total': 0,
            'lecture': 0,
            'practice': 0,
            'trainee': 0,
            'individual': 0
        }
        for lesson in self._lessons:
            hours['total'] += 1
            hours[lesson.type] += 1
        print('hours dict: ', hours)
        return hours

    def _get_journal_template_path(self) -> str:
        """
        Получение пути к файлу шаблона журнала
        :return: путь к файлу
        """
        folder_path = os.path.join(
            settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
            'Шаблоны',
            'Журнал'
        )
        if self.student_group.ou:
            template_name = 'шаблон_ОУ.xlsx'
        else:
            template_name = 'шаблон_ИКУ.xlsx'
        return os.path.join(folder_path, template_name)

    def _get_place(self) -> str:
        """
        Получение места проведения обучения в учебной группе
        :return: строка с местом проведения
        """
        if self.student_group.ou:
            return self.student_group.ou.location
        return self.student_group.iku.location

    def _fill_title_page(self, writer: BookWriter):
        """
        Заполнение титульного листа (первый лист)
        :param writer: объект BookWriter для записи данных в шаблон Excel
        :return:
        """
        department, manager = self._get_department_and_manager()
        date_start, date_end = self._get_date_start_and_end()
        context = {
            'place': self._get_place(),
            'code': self.student_group.code,
            'dep': department,
            'cats': self._get_categories(),
            'manager': manager,
            'day_start': date_start.strftime('%d'),
            'month_start': date_utils.get_month_genitive_case(date_start.strftime('%B')),
            'year_start': date_start.strftime('%Y'),
            'day_end': date_end.strftime('%d'),
            'month_end': date_utils.get_month_genitive_case(date_end.strftime('%B')),
            'year_end': date_end.strftime('%Y')
        }
        if self.student_group.ou:
            program_type, _ = self._get_program_and_certificates_types()
            fio_split = manager.split(' ')
            context['type_dpp'] = program_type
            context['name_dpp'] = self.student_group.ou.program.name
            context['duration'] = self._get_duration()
            context['io_family_manager'] = f'{fio_split[1][:1]} .{fio_split[2][:1]}.{fio_split[0]}'
        writer.render_sheet(context, 'тит', 0)

    def _get_students_list_for_list_page(self) -> list:
        """
        Получение списка с информацией по обучающимся для листа
        со списком обучающихся в группе (второй лист)
        :return:
        """
        students = []


        return students

    def _fill_list_page(self, writer: BookWriter):
        """
        Заполнение листа со списком обучающихся (второй лист)
        :param writer: объект BookWriter для записи данных в шаблон Excel
        :return:
        """

    def _write_book(self):
        """
        Запись данных в книгу Excel
        :return:
        """
        writer = BookWriter(self._get_journal_template_path())
        self._fill_title_page(writer)

