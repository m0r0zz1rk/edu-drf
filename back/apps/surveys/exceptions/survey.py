class SurveyNotExist(Exception):
    """Исключение, вызываемое в случае отсутствия объекта опроса"""
    pass


class SurveyDataNotValid(Exception):
    """Исключение, вызываемое при получении не валидных данных для создания/изменения опроса"""
    pass
