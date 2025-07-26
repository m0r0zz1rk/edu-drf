import os
import re
import uuid
from datetime import date

from xlsxtpl.writerx import BookWriter

from apps.applications.consts.education import STUDENT
from apps.applications.selectors.course_application import course_application_model
from apps.authen.services.profile import profile_service
from apps.commons.utils.data_types.string import string_utils
from apps.commons.utils.django.settings import settings_utils
from apps.docs.services.student_group.base_student_group_doc import BaseStudentGroupDoc
from apps.edu.consts.student_group.forms import WITHOUT
from apps.edu.exceptions.student_group.lessons_not_found import LessonsNotFound, LessonsWithControlNotFound
from apps.edu.serializers.schedule import date_utils
from apps.edu.services.schedule import ScheduleService
from apps.guides.services.mo import mo_service
from apps.guides.services.oo_type import oo_type_service
from apps.guides.services.position_category import position_category_service

_base_student_attributes = ['id', 'surname', 'name', 'patronymic', 'oo', 'pos']

_course_student_attributes = [
    'region',
    'mo',
    'position_category',
    'age',
    'birthday',
    'sex',
    'snils',
    'education_level',
    'diploma_surname',
    'edu_serial',
    'edu_number',
    'type_pay'
]

_event_student_attributes = ['terr', ]

_event_teacher_attributes = ['id', 'fio', 'lecture', 'practice', 'total']

_course_teacher_attributes = [*_event_teacher_attributes, 'trainee', 'individual']


class JournalDoc(BaseStudentGroupDoc):
    """
    Класс для формирования журнала по учебной группе
    """

    _lessons = None
    _schedule_service = None

    class StudentCourseInfo:
        """
        Класс информации для студента на ОУ
        """
        def __init__(self, info: dict):
            """
            Инициализация класса - подстановка значений
            :param info: словарь
            """
            for attribute in [*_base_student_attributes, *_course_student_attributes]:
                setattr(self, attribute, info.get(attribute, '-'))

    class StudentEventInfo:
        """
        Класс информации для студента на ИКУ
        """

        def __init__(self, info: dict):
            """
            Инициализация класса - подстановка значений
            :param info: словарь
            """
            for attribute in [*_base_student_attributes, *_event_student_attributes]:
                setattr(self, attribute, info.get(attribute, '-'))

    class TeacherCourseInfo:
        """
        Класс информации для преподавателя на ОУ
        """
        def __init__(self, info: dict):
            """
            Инициализация класса - подстановка значений
            :param info: словарь
            """
            for attribute in _course_teacher_attributes:
                setattr(self, attribute, info.get(attribute, '-'))

    class TeacherEventInfo:
        """
        Класс информации для преподавателя на ИКУ
        """

        def __init__(self, info: dict):
            """
            Инициализация класса - подстановка значений
            :param info: словарь
            """
            for attribute in _event_teacher_attributes:
                setattr(self, attribute, info.get(attribute, '-'))

    def __init__(self, group_id: uuid):
        """
        Инициализация класса - получение группы, проверка на наличие занятий в расписании
        и наличие занятий с формой проверки
        :param group_id: object_id учебной группы
        """
        super().__init__(group_id)
        self._schedule_service = ScheduleService(group_id)
        self._lessons = self._schedule_service.get_group_lessons()
        if self._lessons.count() == 0:
            raise LessonsNotFound
        if self.student_group.ou:
            if not self._lessons.exclude(control='').exists():
                raise LessonsWithControlNotFound

    def _get_context(self) -> dict:
        pass

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
        else:
            type_name = self.student_group.iku.type.name
            context['type_event'] = string_utils.get_word_case(type_name, 'loct').upper()
            context['event_name'] = self.student_group.iku.name
        writer.render_sheet(context, 'тит', 0)

    @staticmethod
    def _get_application_age(application: course_application_model) -> int:
        """
        Получение возраста на основе заявки обучающегося
        :param application: заявка обучающегося
        :return:
        """
        birthday = application.profile.birthday
        today = date.today()
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    def _get_students_list(self) -> list:
        """
        Получение списка с информацией по обучающимся для листа
        со списком обучающихся в группе (второй лист, листы с ведомостями)
        :return:
        """
        students = []
        for index, application in enumerate(self._get_group_applications(), start=1):
            student_info = {
                'id': index,
                'surname': application.profile.surname,
                'name': application.profile.name,
                'patronymic': application.profile.patronymic,
                'oo': application.oo.short_name if application.oo else application.oo_new,
                'pos': application.position.name if application.position else '-'
            }
            if self.student_group.ou:
                for attribute in _course_student_attributes:
                    if attribute == 'snils':
                        student_info[attribute] = application.profile.snils
                    elif attribute == 'age':
                        student_info[attribute] = self._get_application_age(application)
                    elif attribute == 'birthday':
                        student_info[attribute] = application.profile.birthday.strftime('%d.%m.%Y')
                    elif attribute == 'sex':
                        student_info[attribute] = 'Мужской' if application.profile.sex else 'Женский'
                    elif attribute == 'education_level':
                        student_info[attribute] = application.get_education_level_display()
                    elif attribute == 'education_level':
                        student_info[attribute] = (
                            application.diploma_surname if application.education_level != STUDENT else '-'
                        )
                    elif attribute == 'diploma_surname':
                        student_info[attribute] = (
                            application.diploma_surname if application.education_level != STUDENT else '-'
                        )
                    elif attribute == 'edu_serial':
                        student_info[attribute] = (
                            application.education_serial if application.education_level != STUDENT else '-'
                        )
                    elif attribute == 'edu_number':
                        student_info[attribute] = (
                            application.education_number if application.education_level != STUDENT else '-'
                        )
                    elif attribute == 'type_pay':
                        student_info[attribute] = 'Физ. лицо' if application.physical else 'Юр. лицо'
                    else:
                        student_info[attribute] = (
                            str(getattr(application, attribute)) if getattr(application, attribute, None) else '-'
                        )
            else:
                student_info['terr'] = (
                    f'Иркутская область ({application.mo.name})'
                    if application.region.name == 'Иркутская область' else
                    application.region.name
                )
            if self.student_group.ou:
                students.append(self.StudentCourseInfo(student_info))
            else:
                students.append(self.StudentEventInfo(student_info))
        return students

    def _fill_students_page(self, writer: BookWriter):
        """
        Заполнение листа со списком обучающихся (второй лист)
        :param writer: объект BookWriter для записи данных в шаблон Excel
        :return:
        """
        writer.render_sheet({'students': self._get_students_list()}, 'список', 1)

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
            hours['total'] = hours['total'] + 1
            hours[lesson.type] = hours[lesson.type] + 1
        return hours

    def _get_title_for_teacher_list(self) -> str:
        """
        Получение атрибута title для листа книги Excel с преподавателями (третий лист)
        :return: строка
        """
        res = 'учебной аудиторной нагрузки'
        if self.student_group.form != WITHOUT:
            return (f'{res},\nв т.ч. с использованием электронного обучения '
                    'и дистанционных образовательных технологий')
        return res

    def _get_teachers_for_teachers_page(self) -> list:
        """
        Получение списка с информацией по преподавателям для страницы с преподавателями
        (третий лист)
        :return: список
        """
        teacher_class = self.TeacherEventInfo
        teacher_info_template = {
            'id': 1,
            'fio': '',
            'lecture': 0,
            'practice': 0,
            'total': 0
        }
        if self.student_group.ou:
            teacher_class = self.TeacherCourseInfo
            teacher_info_template['trainee'] = 0
            teacher_info_template['individual'] = 0
        teachers = []
        teachers_ids = set(self._lessons.values_list("teacher", flat=True))
        for index, teacher in enumerate(teachers_ids, start=1):
            teacher_info = dict(teacher_info_template)
            teacher_info['id'] = index
            teacher_info['fio'] = profile_service.get_profile_or_info_by_attribute(
                attribute_name='object_id',
                value=teacher,
                output='display_name'
            )
            teacher_lessons = self._lessons.filter(teacher=teacher)
            for lesson in teacher_lessons:
                teacher_info['total'] += 1
                teacher_info[lesson.type] += 1
            teachers.append(teacher_class(teacher_info))
        return teachers

    def _fill_teachers_page(self, writer: BookWriter):
        """
        Заполнение листа с преподавателями (третий лист)
        :param writer: объект BookWriter для записи данных в шаблон Excel
        :return:
        """
        _, manager = self._get_department_and_manager()
        fio_split = manager.split(' ')
        lessons_count = self._get_lessons_count_by_type()
        context = {
            **lessons_count,
            'short_dep': self._get_department_short_name(),
            'manager': f'{fio_split[1][:1]} .{fio_split[2][:1]}.{fio_split[0]}',
            'title': self._get_title_for_teacher_list(),
            'teachers': self._get_teachers_for_teachers_page()
        }
        writer.render_sheet(context, 'часы ауд', 2)

    def _fill_test_lists(self, writer: BookWriter):
        """
        Заполнение листов с зачетными ведомостями
        :param writer: объект BookWriter для записи данных в шаблон Excel
        :return:
        """
        _, manager = self._get_department_and_manager()
        control_lessons = self._lessons.exclude(control='').order_by('date')
        for index, lesson in enumerate(control_lessons, start=1):
            theme = lesson.theme
            if lesson.kug_theme_id:
                kug_el = self._schedule_service.get_kug_element_by_theme_id(lesson.kug_theme_id)
                theme = kug_el.name
            context = {
                'cats': self._get_categories(),
                'day_lesson': lesson.date.strftime('%d'),
                'month_lesson': date_utils.get_month_genitive_case(lesson.date.strftime('%B')),
                'year_lesson': lesson.date.strftime('%Y'),
                'control_form': lesson.control,
                'manager': manager,
                'theme': theme,
                'students': self._get_students_list()
            }
            if index != len(control_lessons):
                writer.render_sheet(context, f'Зачетная ведомость ПА {2 - index}', 3)
            else:
                writer.render_sheet(context, f'Зачетная ведомость ИА', 4)

    @staticmethod
    def get_dict_with_all_object(class_service) -> list:
        """
        Получение словаря со всеми объектами для статистики (МО, Тип ОО, Должность)
        :return:
        """
        objects = class_service.get_all()
        obj_dict = []
        for index, obj in enumerate(objects, start=1):
            obj_dict.append({
                'id': index,
                'name': obj.name,
                'count': 0
            })
        return obj_dict

    def _fill_statistics_list(self, writer: BookWriter):
        """
        Заполнение листа со статистикой (четвертый лист для ИКУ)
        :param writer: объект BookWriter для записи данных в шаблон Excel
        :return:
        """
        context = {
            'mos': self.get_dict_with_all_object(mo_service),
            'oo_types': self.get_dict_with_all_object(oo_type_service),
            'position_categories': self.get_dict_with_all_object(position_category_service)
        }
        applications = self._get_group_applications()
        for application in applications:
            mapping = {
                'mos': application.mo.name,
                'oo_types': application.oo.oo_type.name,
                'position_categories': application.position_category.name
            }
            for key, value in mapping.items():
                for obj in context[key]:
                    if obj['name'] == value:
                        obj['count'] += 1
                        break
        writer.render_sheet(context, f'стат', 3)

    def _generate_wb(self):
        """
        Запись данных в книгу Excel
        :return:
        """
        writer = BookWriter(self._get_journal_template_path())
        self._fill_title_page(writer)
        self._fill_students_page(writer)
        self._fill_teachers_page(writer)
        if self.student_group.ou:
            self._fill_test_lists(writer)
        else:
            self._fill_statistics_list(writer)
        return writer
