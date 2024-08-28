class LessonTimeUtils:
    """Класс методов для работы с временем начала и окончания занятий в расписании учебной группы"""

    @staticmethod
    def convert_seconds_to_time(seconds: int) -> str:
        """
        Конвертация количества секунд во время в формате ЧЧ:ММ
        :param seconds: Количество секунд
        :return: Время в формате ЧЧ:ММ
        """
        if seconds < 0:
            return '-'
        time = ''
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        if hours < 10:
            time += f'0{hours}'
        else:
            time += f'{hours}'
        if minutes < 10:
            time += f'0{minutes}'
        else:
            time += f'{minutes}'
        return time
