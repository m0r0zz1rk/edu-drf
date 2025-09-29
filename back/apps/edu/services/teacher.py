import datetime
import uuid

from django.db.models import Q

from apps.commons.utils.data_types.date import date_utils
from apps.edu.selectors.schedule import schedule_orm


class TeacherService:
    """Класс методов для работы с преподавателями в расписании занятий"""

    @staticmethod
    def check_teacher_busy(teacher_id: uuid, group_id: uuid, day: datetime.date, time_start_str: str) -> bool:
        """
        Проверка занятости преподавателя
        :param teacher_id: object_id объекта модели CokoProfile или StudentProfile
        :param group_id: object_id учебной группы
        :param day: Дата проведения занятия
        :param time_start_str: Время начала занятия в формате ЧЧ:ММ
        :return: True - преподаватель свободен, False - преподаватель занят
        """
        time_start = date_utils.convert_time_string_to_seconds(time_start_str)
        lessons = schedule_orm.get_filter_records(filter_by={'date': day, 'teacher': teacher_id})
        lessons = lessons.filter(Q(time_start__lte=time_start) & Q(time_end__gt=time_start))
        if lessons.count() == 0:
            return True
        if lessons.count() == 1:
            if str(lessons.first().group_id) == str(group_id):
                return True
        return False
