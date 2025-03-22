from django.db.models import QuerySet

from apps.edu.consts.student_group.statuses import REGISTRATION
from apps.edu.selectors.student_group import student_group_queryset


def events_queryset() -> QuerySet:
    """
    Получение queryset с группами, основанными на мероприятиях,
    и со статусом "Регистрация"
    """
    return student_group_queryset().filter(ou=None).filter(status=REGISTRATION)
