class LessonsNotFound(Exception):
    """
    Исключение, вызываемое при отсутствии занятий в расписании у учебной группы
    """
    pass


class LessonsWithControlNotFound(Exception):
    """
    Исключение, вызываемое при отсутствии занятий с формой контроля у учебной группы
    """
    pass
