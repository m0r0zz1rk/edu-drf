import uuid

from django.apps import apps
from django.db.models import QuerySet

schedule_model = apps.get_model('edu', 'Schedule')


def schedule_queryset(student_group_id: uuid = None) -> QuerySet:
    """
    Получение расписания занятий для учебной группы
    :param student_group_id: object_id учебной группы
    :return: queryset модели schedule
    """
    if student_group_id is None:
        return schedule_model.objects.all().order_by('date')
    return schedule_model.objects.filter(group_id=student_group_id).order_by('date')
