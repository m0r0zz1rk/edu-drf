from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.authen.serializers.states_serializer import StatesSerializer
from apps.commons.consts.journals.journal_event_results import ERROR
from apps.commons.consts.journals.journal_rec_types import STATES
from apps.commons.utils.django.response import ResponseUtils
from apps.authen.utils.state import StateUtils
from apps.journals.writer.journal_writer import JournalWriter


class StatesViewSet(viewsets.ViewSet):
    """API для работы с государствами"""

    journal = JournalWriter(STATES)

    @swagger_auto_schema(
        tags=['Профиль', ],
        operation_description="Получение списка государств",
        responses={
            '400': 'Ошибка при попытке получить список (сообщение "Повторите попытку позже" или ошибка)',
            '200': StatesSerializer}
    )
    def get_states(self, request, *args, **kwargs):
        """Получение списка государств"""
        ru = ResponseUtils()
        states_info = StateUtils.get_all_states()
        serialize = StatesSerializer(data=states_info)
        if serialize.is_valid(raise_exception=True):
            return ru.ok_response_dict(serialize.data)
        else:
            self.journal.write(
                'Система',
                ERROR,
                'Ошибка при получении списка государств: не пройдена сериализация данных'
            )
            return ru.sorry_try_again_response()
