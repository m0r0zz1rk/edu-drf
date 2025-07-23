import os
import uuid

from xlsxtpl.writerx import BookWriter

from apps.authen.services.profile import profile_service
from apps.commons.utils.django.settings import settings_utils
from apps.docs.services.student_group.base_student_group_doc import BaseStudentGroupDoc
from apps.edu.consts.lesson_types import LECTURE, PRACTICE, INDIVIDUAL
from apps.edu.exceptions.student_group.lessons_not_found import LessonsNotFound, LessonsWithControlNotFound
from apps.edu.serializers.schedule import date_utils
from apps.edu.services.schedule import ScheduleService


class ScheduleDoc(BaseStudentGroupDoc):
    """
    Класс для получения Excel файла с расписанием занятий учебной группы
    """

    _week_days = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье'
    }

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

    def _get_schedule_template_path(self) -> str:
        """
        Получение пути к файлу шаблона расписания
        :return: путь к файлу
        """
        folder_path = os.path.join(
            settings_utils.get_parameter_from_settings('MEDIA_ROOT'),
            'Шаблоны',
            'Расписание'
        )
        if self.student_group.ou:
            template_name = 'шаблон_ОУ.xlsx'
        else:
            template_name = 'шаблон_ИКУ.xlsx'
        return os.path.join(folder_path, template_name)

    def _get_lessons_info(self) -> list:
        """
        Получение списка информации по занятиям
        :return: список с информацией по занятиям
        """
        result = []
        for lesson in self._lessons:
            time_start = date_utils.convert_seconds_to_time_string(lesson.time_start)
            time_end = date_utils.convert_seconds_to_time_string(lesson.time_end)
            teacher = '-' if not lesson.teacher else profile_service.get_profile_or_info_by_attribute(
                'object_id',
                lesson.teacher,
                'display_name'
            )
            obj = {
                'weekday': self._week_days.get(lesson.date.weekday()),
                'date': lesson.date.strftime('%d.%m.%Y'),
                'time': f'{time_start} - {time_end}',
                'theme': lesson.kug_theme.name if lesson.kug_theme else lesson.theme,
                'lecture': '1' if lesson.type == LECTURE else '0',
                'practice': '1' if lesson.type == PRACTICE else '0',
                'teacher': teacher
            }
            if self.student_group.ou:
                obj['individual'] = '1' if lesson.type == INDIVIDUAL else '0'
            result.append(obj)
        return result

    def _fill_schedule_page(self, writer: BookWriter):
        """
        Заполнение листа со списком занятий
        :param writer: объект BookWriter для записи данных в шаблон Excel
        :return:
        """
        dep, manager = self._get_department_and_manager()
        date_start, date_end = self._get_date_start_and_end()
        hours = self._get_lessons_count_by_type()
        info = {
            'dep': dep,
            'code': self.student_group.code,
            'cats': self._get_audience_categories_str(),
            'day_start': date_start.strftime('%d'),
            'month_start': date_utils.get_month_genitive_case(date_start.strftime('%B')),
            'year_start': date_start.strftime('%Y'),
            'day_finish': date_end.strftime('%d'),
            'month_finish': date_utils.get_month_genitive_case(date_end.strftime('%B')),
            'year_finish': date_end.strftime('%Y'),
            'total_lecture': hours.get('lecture', 0),
            'total_practice': hours.get('practice', 0),
            'total_hours': hours.get('total', 0),
            'short_dep': self._get_department_short_name(),
            'io_family_manager': manager,
            'items': self._get_lessons_info()
        }
        if self.student_group.ou:
            info['name'] = self.student_group.ou.program.name
            info['total_individual'] = hours.get('individual', 0)
        else:
            info['name'] = self.student_group.iku.name
        writer.render_sheet(info, 'Расписание', 1)

    def _generate_wb(self):
        """
        Запись данных в книгу Excel
        :return:
        """
        writer = BookWriter(self._get_schedule_template_path())
        self._fill_schedule_page(writer)
        return writer
