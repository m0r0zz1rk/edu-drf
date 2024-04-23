import uuid

from apps.celery_app.models import UserEventEmails


class UserEventEmailsUtils:
    """Класс методов для проверки отправленных сообщений по мероприятиям"""

    @staticmethod
    def check_event_published(user_id: int, event_id: uuid) -> bool:
        """Проверка на отправленное сообщение об опубликованном мероприятии"""
        return UserEventEmails.objects.filter(user_id=user_id).filter(event_id=event_id). \
            filter(event_published=True).exists()

    @staticmethod
    def check_event_start_tomorrow(user_id: int, event_id: uuid) -> bool:
        """Проверка на отправленное сообщение о завтрашнем начале мероприятия"""
        return UserEventEmails.objects.filter(user_id=user_id).filter(event_id=event_id). \
            filter(event_start_tomorrow=True).exists()

    @staticmethod
    def check_event_start_today(user_id: int, event_id: uuid) -> bool:
        """Проверка на отправленное сообщение о сегодняшнем начале мероприятия"""
        return UserEventEmails.objects.filter(user_id=user_id).filter(event_id=event_id). \
            filter(event_start=True).exists()

    @staticmethod
    def create_rec_event(user_id: int, event_id: uuid, type: str):
        """Создание или редактирование записи о мероприятии (мероприятие опубликовано)"""
        rec, _ = UserEventEmails.objects.get_or_create(
            user_id=user_id,
            event_id=event_id
        )
        match type:
            case 'PUBLISHED':
                rec.event_published = True

            case 'TOMORROW':
                rec.event_start_tomorrow = True

            case 'TODAY':
                rec.event_start = True

            case _:
                pass
        rec.save()
