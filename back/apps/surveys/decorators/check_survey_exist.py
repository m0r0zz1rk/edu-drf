from functools import wraps
from typing import Optional

from apps.surveys.exceptions.survey import SurveyNotExist
from apps.surveys.selectors.survey import survey_model


def check_survey_exist(survey: Optional[survey_model]):
    """Декоратор для проверки наличия объекта опроса"""
    def inner_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if survey is None:
                raise SurveyNotExist
            return func(*args, **kwargs)
        return wrapper
    return inner_decorator
