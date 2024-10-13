from django.db.models import QuerySet

from apps.edu.consts.student_group.student_group_statuses import REGISTRATION
from apps.edu.selectors.student_group import student_group_queryset


def courses_queryset() -> QuerySet:
    """
    Получение queryset с группами, основанными на курсах,
    и со статусом "Регистрация"
    """
    return student_group_queryset().filter(iku=None).filter(status=REGISTRATION)
