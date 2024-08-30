import datetime
import uuid
from datetime import timedelta
from datetime import datetime as dt

from apps.edu.selectors.schedule import schedule_model
from apps.edu.selectors.student_group import student_group_model
from apps.edu.services.service.education_service import EducationServiceService
from apps.edu.services.service.information_service import InformationServiceService
from apps.edu.services.student_group import StudentGroupService


class ScheduleService:
    """Класс методов для работы с расписаниями учебной группы"""

    __group_id = None

    __student_group_service = StudentGroupService()
    __education_service = EducationServiceService()
    __information_service = InformationServiceService()

    def __init__(self, group_id: uuid):
        """
        Инициализация класса - установка статического атрибута object_id учбеной группы
        :param group_id: object_id учбеной группы - объекта StudentGroup
        """
        self.__group_id = group_id

    def get_period_borders(self, student_group: student_group_model) -> list:
        """
        Получение границ периода обучения группы
        :param student_group: Объект модели StudentGroup
        :return: список
        """
        if student_group.ou:
            date_init = self.__education_service.get_info_by_service(
                'object_id',
                student_group.ou.object_id,
                'date_start'
            )
            date_complete = self.__education_service.get_info_by_service(
                'object_id',
                student_group.ou.object_id,
                'date_end'
            )
        else:
            date_init = self.__information_service.get_info_by_service(
                'object_id',
                student_group.iku.object_id,
                'date_start'
            )
            date_complete = self.__information_service.get_info_by_service(
                'object_id',
                student_group.iku.object_id,
                'date_end'
            )
        return [date_init, date_complete]

    def get_dates_list(self) -> list:
        """
        Получение списка дней с занятиями учебной группы
        :return: список дней
        """
        days_list = []
        student_group = self.__student_group_service.get_student_group(
            'object_id',
            self.__group_id
        )
        if student_group:
            borders = self.get_period_borders(student_group)
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
        return [lesson for lesson in schedule_model.objects.filter(
            date=day
        ).filter(
            group_id=self.__group_id
        ).order_by('time_start')]

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
