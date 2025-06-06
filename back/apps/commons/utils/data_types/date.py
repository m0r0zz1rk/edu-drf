import datetime
import re
import time
from typing import Optional

from apps.commons.exceptions.date.incorrect_time_format import IncorrectTimeFormatError


class DateUtils:
    """Валидаторы и методы для даты/даты и времени"""

    _month_genitive_case = {
        'January': 'января',
        'February': 'февраля',
        'March': 'марта',
        'April': 'апреля',
        'May': 'мая',
        'June': 'июня',
        'July': 'июля',
        'August': 'августа',
        'September': 'сентября',
        'October': 'октября',
        'November': 'ноября',
        'December': 'декабря',
    }

    @staticmethod
    def is_object_date(obj) -> bool:
        """Проверка является ли объект датой"""
        return isinstance(obj, datetime.datetime)

    @staticmethod
    def convert_str_to_date(date: str):
        """Преобразование строковой даты ДД-ММ-ГГГГ в python datetime"""
        try:
            return datetime.datetime.strptime(date, '%d.%m.%Y')
        except BaseException:
            return None

    @staticmethod
    def convert_date_to_str(date: datetime.date) -> str:
        """Преобразование даты в строку формата: дд.мм.гггг"""
        if date is not None:
            return date.strftime("%d.%m.%Y")
        return None

    @staticmethod
    def convert_datetime_to_str(date: datetime.datetime) -> Optional[str]:
        """Преобразование даты в строку формата: дд.мм.гггг"""
        if date is not None:
            return date.strftime("%d.%m.%Y %H:%m")
        return None

    def convert_obj_to_date(self, obj):
        if self.is_object_date(obj):
            return obj.strftime("%d.%m.%Y")
        else:
            try:
                return datetime.date(obj).strftime("%d.%m.%Y")
            except Exception:
                return None

    @staticmethod
    def convert_html_date(obj) -> Optional[datetime.date]:
        """Конвертирование даты с HTML формы в дату для python"""
        try:
            return datetime.datetime.strptime(obj, '%Y-%m-%d')
        except BaseException:
            try:
                return datetime.datetime.strptime(obj, '%d.%m.%Y')
            except BaseException:
                return None

    @staticmethod
    def split_date_range(date_range: str) -> Optional[list]:
        """Разделить значение из компонента ui5-daterange-picker на две даты"""
        dates = date_range.split(' - ')
        if len(dates) != 2:
            return None
        try:
            date_start = datetime.datetime.strptime(
                dates[0],
                '%d.%m.%Y'
            )
            date_end = datetime.datetime.strptime(
                dates[1],
                '%d.%m.%Y'
            )
            return [date_start, date_end]
        except Exception:
            return None

    def check_cross_and_second_after_first_date_ranges(self, first_dr: str, second_dr: str) -> bool:
        """Проверка на пересечение временных интервалов и их последовательность"""
        first_dr_dates = self.split_date_range(first_dr)
        second_dr_dates = self.split_date_range(second_dr)
        if first_dr_dates[0] >= second_dr_dates[0] or first_dr_dates[1] >= second_dr_dates[0]:
            return True
        return False

    @staticmethod
    def convert_time_string_to_seconds(time_string: str) -> int:
        """
        Преобразование времени в формате ЧЧ:ММ в количество секунд
        :param time_string: время в формате ЧЧ:ММ
        :return: количество секунд
        """
        pattern = re.compile("[0-9]{2}:[0-9]{2}")
        if not pattern.match(time_string):
            raise IncorrectTimeFormatError
        hours, minutes = time_string.split(':')[0], time_string.split(':')[1]
        return int(hours) * 60 * 60 + int(minutes) * 60

    @staticmethod
    def convert_seconds_to_time_string(seconds: int) -> str:
        """
        Преобразование количества секунд в текстовый формат времени: ЧЧ:ММ
        :param seconds: количество секунд
        :return: время в формате ЧЧ:ММ
        """
        return time.strftime('%H:%M', time.gmtime(seconds))

    def get_month_genitive_case(self, month: str) -> str:
        """
        Получение родительного падежа для полученного названия месяца
        :param month: название месяца (с большой буквы)
        :return: родительный падеж
        """
        return self._month_genitive_case[month]

    def get_text_date_genitive_case(self, date: datetime) -> str:
        """
        Получение текстового представления даты (ДД месяц ГГГГ г.) в родительном падеже
        :param date: исходная дата
        :return: дата в родительном падеже
        """
        return (f'{date.strftime("%d")} '
               f'{self.get_month_genitive_case(date.strftime("%B"))} '
               f'{date.strftime("%Y")} года')


date_utils = DateUtils()
