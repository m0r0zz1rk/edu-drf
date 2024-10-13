from django.apps import apps
from django.db.models import QuerySet

event_application_model = apps.get_model('applications', 'EventApplication')


def event_application_queryset() -> QuerySet:
    """Получение queryset со всем заявками на участие в мероприятиях"""
    return event_application_model.objects.all().order_by(
        'profile__surname',
        'profile__name',
        'profile__patronymic'
    )
