from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.admins.serializers.centre_main_page_serializer import CentreMainPageSerializer
from apps.admins.utils.main_page import MainPageUtils
from apps.authen.utils.profile import ProfileUtils
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.response import ResponseUtils
from apps.journal.consts.journal_modules import ADMINS
from apps.journal.consts.journal_rec_statuses import JOURNAL_REC_STATUSES, ERROR
from apps.journal.utils.journal_utils import JournalUtils


class MainPageViewSet(viewsets.ViewSet):
    """Работа с главной страницей ЛК администратора АИС"""
    permission_classes = [IsAuthenticated, IsAdministrators]

    ju = JournalUtils()
    pu = ProfileUtils()
    mpu = MainPageUtils()
    respu = ResponseUtils()

    def _endpoint_rec_journal(
        self,
        user_id: int,
        message_type: JOURNAL_REC_STATUSES,
        description: str,
        payload: str,
        output: str = None
    ):
        """
        Внесение записи в журнал событий
        :param message_type: Тип сообщения в журнале событий
        :param user_id: ID пользователя Django
        :param description: описание ошибки
        :param payload: полезная нагрузка
        :param output: выходные данные (при наличии
        :return:
        """
        self.ju.create_journal_rec(
            {
                'source': self.pu.get_profile_or_info_by_attribute(
                    'django_user_id',
                    user_id,
                    'display_name'
                ),
                'module': ADMINS,
                'status': message_type,
                'description': description
            },
            payload,
            output
        )

    @swagger_auto_schema(
        tags=['Администраторы', ],
        operation_description="Получение информации для главной страницы (для администраторов)",
        responses={
            '400': 'Сообщение "Повторите попытку позже"',
            '403': 'Пользователь не авторизован или не является администратором',
            '200': CentreMainPageSerializer}
    )
    def get_main_page_centre(self, request, *args, **kwargs):
        info = self.mpu.get_information(request)
        print(info)
        serialize = CentreMainPageSerializer(data=info)
        if serialize.is_valid():
            return self.respu.ok_response_dict(serialize.data)
        else:
            self._endpoint_rec_journal(
                request.user.id,
                ERROR,
                'Ошибка при получении данных для главной страницы - данные не прошли валидацию',
                repr(info),
                repr(serialize.errors)
            )
            return self.respu.sorry_try_again_response()
