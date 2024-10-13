import datetime
import uuid
from datetime import timedelta
from datetime import datetime as dt

from apps.authen.services.profile import ProfileService
from apps.commons.exceptions.date.incorrect_time_format import IncorrectTimeFormatError
from apps.commons.utils.data_types.date import DateUtils
from apps.edu.consts.lesson_types import LESSON_TYPES
from apps.edu.exceptions.calendar_chart.incorrect_theme_dict_format import IncorrectThemeDictFormat
from apps.edu.exceptions.schedule.day_info_validate_error import DayInfoValidateError
from apps.edu.exceptions.schedule.schedule_generate_error import ScheduleGenerateError
from apps.edu.exceptions.student_group.student_group_not_found import StudentGroupNotFound
from apps.edu.selectors.schedule import schedule_model
from apps.edu.services.service.education_service import EducationServiceService
from apps.edu.services.service.information_service import InformationServiceService
from apps.edu.services.student_group import StudentGroupService


class ScheduleService:
    """Класс методов для работы с расписаниями учебной группы"""

    __group = None

    __student_group_service = StudentGroupService()
    __education_service = EducationServiceService()
    __information_service = InformationServiceService()
    __date_utils = DateUtils()

    __lesson_template = {
        'group_id': None,
        'date': datetime.date.today(),
        'time_start': 0,
        'time_end': 0,
    }

    __lesson_keys = [
        "time_start_str",
        "time_end_str",
        "kug_theme_id",
        "theme",
        "type",
        "teacher_fio",
        "teacher",
        "distance",
        "control"
    ]

    __day_info_keys = [
        'day',
        'group_id',
        'lessons'
    ]

    def __init__(self, group_id: uuid):
        """
        Инициализация класса - установка статического атрибута object_id учбеной группы
        :param group_id: object_id учбеной группы - объекта StudentGroup
        """
        self.__group = self.__student_group_service.get_student_group(
            'object_id',
            group_id
        )

    def get_period_borders(self) -> list:
        """
        Получение границ периода обучения группы
        :return: список, содержащий даты начала и окончания периода обучения
        """
        if not self.__group:
            raise StudentGroupNotFound
        if self.__group.ou:
            date_init = self.__education_service.get_info_by_service(
                'object_id',
                self.__group.ou.object_id,
                'date_start'
            )
            date_complete = self.__education_service.get_info_by_service(
                'object_id',
                self.__group.ou.object_id,
                'date_end'
            )
        else:
            date_init = self.__information_service.get_info_by_service(
                'object_id',
                self.__group.iku.object_id,
                'date_start'
            )
            date_complete = self.__information_service.get_info_by_service(
                'object_id',
                self.__group.iku.object_id,
                'date_end'
            )
        return [date_init, date_complete]

    def get_dates_list(self) -> list:
        """
        Получение списка дней с занятиями учебной группы
        :return: список дней
        """
        days_list = []
        try:
            borders = self.get_period_borders()
        except StudentGroupNotFound:
            pass
        else:
            while dt.strptime(borders[1], '%d.%m.%Y') >= dt.strptime(borders[0], '%d.%m.%Y'):
                days_list.append(borders[0])
                new_date = dt.strptime(borders[0], '%d.%m.%Y') + timedelta(days=1)
                borders[0] = new_date.strftime('%d.%m.%Y')
        return days_list

    def get_lessons_for_day(self, day: datetime.date) -> list:
        """
        Получение списка занятий учебного дня
        :param day: дата учебного дня
        :return: список занятий
        """
        lessons = []
        for lesson in schedule_model.objects.filter(
                date=day
        ).filter(
            group_id=self.__group.object_id
        ).order_by('time_start'):
            voc = dict({
                'kug_theme_id': lesson.kug_theme_id
            })
            for field in schedule_model._meta.get_fields():
                if field.name in ['object_id', 'date_create', 'group', 'date']:
                    continue
                else:
                    voc[field.name] = getattr(lesson, field.name)
            lessons.append(voc)
        try:
            del voc
        except Exception:
            pass
        return lessons

    def get_group_schedule(self) -> list:
        """
        Получение списка занятий по дням для учебной группы
        """
        schedule = []
        days = self.get_dates_list()
        for day in days:
            schedule.append({
                'day': day,
                'lessons': self.get_lessons_for_day(dt.strptime(day, '%d.%m.%Y'))
            })
        return schedule

    def check_day_lessons(self, day: datetime.date) -> bool:
        """
        Проврека наличия учебного дня у учебной группы
        :param day: объект datetime, проверяемый день
        """
        if not self.__group:
            raise StudentGroupNotFound
        period = self.get_dates_list()
        return day.strftime('%d.%m.%Y') in period

    def delete_day_lessons(self, day: datetime.date):
        """
        Удаление занятий учебной группы за определенный день
        :param day: объект datetime, день занятий
        """
        if not self.__group:
            raise StudentGroupNotFound
        if self.check_day_lessons(day):
            for lesson in schedule_model.objects.filter(
                    date=day
            ).filter(
                group_id=self.__group.object_id
            ):
                lesson.delete()

    def generate_schedule(self, generate_days: list):
        """
        Генерация расписания для учебной группы
        :param generate_days: список параметров для каждого учебного дня группы
        """
        try:
            for day in generate_days:
                if day['study_day']:
                    dt_day = dt.strptime(day['day'], '%d.%m.%Y')
                    self.delete_day_lessons(dt_day)
                    try:
                        time_start = self.__date_utils.convert_time_string_to_seconds(day['time_start'])
                    except IncorrectTimeFormatError:
                        raise ScheduleGenerateError
                    self.__lesson_template['group_id'] = self.__group.object_id
                    self.__lesson_template['date'] = dt_day
                    self.__lesson_template['time_start'] = time_start
                    self.__lesson_template['time_end'] = time_start + (45 * 60)
                    schedule_model.objects.create(**self.__lesson_template)
                    if int(day['hours_count']) > 1:
                        for index in range(2, int(day['hours_count']) + 1):
                            if index == 5:
                                time_start += (75 * 60)  # Обеденный перерыв после 4-го занятия - 30 минут
                            else:
                                if index % 2 == 0:
                                    time_start += 45 * 60  # Второе занятие начинается сразу
                                else:
                                    time_start += 55 * 60  # Между парами перерыв 10 минут
                            self.__lesson_template['time_start'] = time_start
                            self.__lesson_template['time_end'] = time_start + (45 * 60)
                            schedule_model.objects.create(**self.__lesson_template)
        except RuntimeError:
            raise ScheduleGenerateError

    def get_remain_hours_for_kug_theme(self, theme: dict) -> dict:
        """
        Получить словарь с остаточным количеством часов по теме КУГ
        :param theme: Словарь с часами темы КУГ
        :return: Словарь с остаточными часами в расписании учебной группы
        """
        remain_hours = {}
        keys = [
            'chapter',
            'theme',
            'theme_id',
            'lecture',
            'practice',
            'trainee',
            'individual'
        ]
        for key, value in theme.items():
            if key not in keys:
                raise IncorrectThemeDictFormat
            else:
                remain_hours[key] = value
        schedule = self.get_group_schedule()
        for day in schedule:
            for lesson in day['lessons']:
                if lesson['kug_theme_id'] == theme['theme_id']:
                    remain_hours[lesson['type']] -= 1
        return remain_hours

    def validate_day_info(self, day_info_object: dict):
        """
        Валидация информации об учебном дне
        """
        for key in day_info_object:
            if key not in self.__day_info_keys:
                print(key)
                raise DayInfoValidateError
        for lesson in day_info_object['lessons']:
            for key in lesson:
                if key not in self.__lesson_keys:
                    print(key)
                    raise DayInfoValidateError

    def save_lesson(
            self,
            lesson_info: dict,
            day: datetime.date
    ):
        """
        Сохранение занятия в расписание
        :param lesson_info: объект с информацией по занятию
        :param day: учебный день
        """
        time_start = self.__date_utils.convert_time_string_to_seconds(lesson_info['time_start_str'])
        time_end = self.__date_utils.convert_time_string_to_seconds(lesson_info['time_end_str'])
        del lesson_info['time_start_str']
        del lesson_info['time_end_str']
        lesson_object = {
            'group_id': self.__group.object_id,
            'date': day,
            'time_start': time_start,
            'time_end': time_end,
            **lesson_info
        }
        schedule_model.objects.create(**lesson_object)

    def save_day_info(self, day_info_object: dict):
        """
        Сохранение информации по занятиям учебного дня
        :param day_info_object: объект учебного дня
        """
        del day_info_object['group_id']
        self.validate_day_info(day_info_object)
        self.delete_day_lessons(
            datetime.datetime.strptime(day_info_object['day'], '%Y-%m-%d')
        )
        for lesson in day_info_object['lessons']:
            self.save_lesson(
                lesson,
                day_info_object['day']
            )

    def get_personal_schedule(self, user_id: int):
        """
        Получение личного расписания преподавателя
        :param user_id: ID пользователя Django
        """
        profile = ProfileService().get_profile_or_info_by_attribute(
            'django_user_id',
            user_id,
            'profile'
        )
        days = {lesson.date for lesson in schedule_model.objects.filter(teacher=profile.object_id)
                if lesson.date > datetime.date.today()}
        schedule = []
        for day in days:
            day_lessons = schedule_model.objects.filter(
                date=day,
                teacher=profile.object_id
            ).order_by('date_create')
            lessons = []
            for lesson in day_lessons:
                obj = {
                    'group_code': lesson.group.code,
                    'time_start_str': self.__date_utils.convert_seconds_to_time_string(lesson.time_start),
                    'time_end_str': self.__date_utils.convert_seconds_to_time_string(lesson.time_end),
                    'distance': lesson.distance,
                    'control': lesson.control
                }
                for t in LESSON_TYPES:
                    if t[0] == lesson.type:
                        obj['type'] = t[1]
                if lesson.kug_theme:
                    obj['lesson_theme'] = lesson.kug_theme.name
                else:
                    obj['lesson_theme'] = lesson.theme
                lessons.append(obj)
            schedule.append({
                'date': day.strftime('%d.%m.%Y'),
                'lessons': lessons
            })
        return schedule
