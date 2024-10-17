from django.apps import apps
from django.db.models import QuerySet

event_application_model = apps.get_model('applications', 'EventApplication')


def event_application_queryset() -> QuerySet:
    """Получение queryset со всем заявками на участие в мероприятиях"""
    return (event_application_model.objects.
            select_related('profile').
            select_related('group').
            select_related('pay_doc').
            select_related('region').
            select_related('mo').
            select_related('oo').
            select_related('position_category').
            select_related('position').
            all().order_by(
                'profile__surname',
                'profile__name',
                'profile__patronymic'
            ))
