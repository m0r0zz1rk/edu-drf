from django.apps import apps
from django.db.models import QuerySet

course_application_model = apps.get_model('applications', 'CourseApplication')


def course_application_queryset() -> QuerySet:
    """Получение queryset со всем заявками на участие в курсах"""
    return course_application_model.objects.all().order_by(
        'profile__surname',
        'profile__name',
        'profile__patronymic'
    )
