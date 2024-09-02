import datetime
import uuid
from datetime import timedelta
from datetime import datetime as dt

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
        return [lesson for lesson in schedule_model.objects.filter(
            date=day
        ).filter(
            group_id=self.__group.object_id
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

    def check_day_lessons(self, day: datetime.date) -> bool:
        """
        Проврека наличия учебного дня у учебной группы
        :param day: объект datetime, проверяемый день
        """
        if not self.__group:
            raise StudentGroupNotFound
        period = self.get_dates_list()
        return day.strftime('%d.%m.%Y') in period

    def delete_day_lessons(self, day: datetime.date, group_id: uuid):
        """
        Удаление занятий учебной группы за определенный день
        :param day: объект datetime, день занятий
        :param group_id: объект uuid, object_id учебной группы
        """
        group = self.__student_group_service.get_student_group(
            'object_id',
            group_id
        )
        if not group:
            raise StudentGroupNotFound
        if self.check_day_lessons(day):
            for lesson in self.get_lessons_for_day(day):
                lesson.delete()

    def generate_schedule(self, generate_days: list):
        """
        Генерация расписания для учебной группы
        :param generate_days: список параметров для каждого учебного дня группы
        """


