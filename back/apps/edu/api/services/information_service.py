from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.authen.services.profile import ProfileService
from apps.commons.pagination import CustomPagination
from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.utils.django.exception import ExceptionHandling
from apps.commons.utils.django.request import RequestUtils
from apps.commons.utils.django.response import ResponseUtils
from apps.edu.operations.service.add_update import AddUpdateService
from apps.edu.operations.service.delete import DeleteService
from apps.edu.selectors.services.information_service import information_service_queryset, InformationServiceFilter

from apps.edu.serializers.services.information_service import InformationServiceListSerializer, \
    InformationServiceRetrieveAddUpdateSerializer
from apps.edu.services.service.information_service import InformationServiceService
from apps.edu.services.program import ProgramService
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class InformationServiceViewSet(viewsets.ModelViewSet):
    """Работа с информационно-консультационными услугами (мероприятиями)"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    ru = RequestUtils()
    ju = JournalService()
    pu = ProfileService()
    pru = ProgramService()
    iss = InformationServiceService()
    respu = ResponseUtils()

    queryset = information_service_queryset()
    lookup_field = "object_id"
    serializer_class = InformationServiceListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = InformationServiceFilter

    @swagger_auto_schema(
        tags=['Учебная часть. Информационно-консультационные услуги', ],
        operation_description="Получение списка ИК услуг (мероприятий)",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': InformationServiceListSerializer(many=True)
        }
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return self.respu.ok_response_dict(serializer.data)
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Ошибка при получении списка ИК услуг (мероприятий)'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Учебная часть. Информационно-консультационные услуги', ],
        operation_description="Получение объекта ИК услуги (мероприятия)",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении объекта',
            '200': InformationServiceRetrieveAddUpdateSerializer
        }
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = InformationServiceRetrieveAddUpdateSerializer(
                self.iss.prepare_to_serialize(instance.object_id)
            )
            return self.respu.ok_response_dict(serializer.data)
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Системная ошибка при получении объекта ИК услуги (мероприятия)'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Учебная часть. Информационно-консультационные услуги', ],
        operation_description="Добавление/обновление ИК услуги (мероприятия)",
        request_body=InformationServiceRetrieveAddUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении/обновлении ИК услуги (мероприятия)',
            '200': 'Сообщение "Информационно-консультационная услуга успешно добавлена/обновлена"'
        }
    )
    def create_update(self, request, *args, **kwargs):
        serialize = InformationServiceRetrieveAddUpdateSerializer(data=request.data)
        if serialize.is_valid():
            process = AddUpdateService(
                {
                    'source': self.pu.get_profile_or_info_by_attribute(
                        'django_user_id',
                        request.user.id,
                        'display_name'
                    ),
                    'module': EDU,
                    'process_data': dict(serialize.validated_data)
                },
                'info',
                request
            )
            if process.process_completed:
                return self.respu.ok_response('Информационно-консультационная услуга успешно добавлена/обновлена')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            return self.respu.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=['Учебная часть. Информационно-консультационные услуги', ],
        operation_description="Удаление ИК услуги (мероприятия)",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при удалении ИК услуги (мероприятия)',
            '200': 'Сообщение "Информационно-консультационная услуга успешно удалена"'
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            proc = DeleteService(
                {
                    'source': self.pu.get_profile_or_info_by_attribute(
                        'django_user_id',
                        request.user.id,
                        'display_name'
                    ),
                    'module': EDU,
                    'process_data': {'object_id': instance.object_id}
                },
                'info',
                request
            )
            if proc.process_completed:
                return self.respu.ok_response('Информационно-консультационная услуга успешно удалена')
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Системная ошибка при удалении ИК услуги (курса)'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
        return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
