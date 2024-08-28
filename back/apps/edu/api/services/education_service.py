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
from apps.edu.selectors.services.education_service import education_service_queryset, EducationServiceFilter

from apps.edu.serializers.services.education_service import EducationServiceListSerializer, \
    EducationServiceRetrieveSerializer, EducationServiceAddUpdateSerializer
from apps.edu.services.program import ProgramService
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class EducationServiceViewSet(viewsets.ModelViewSet):
    """Работа с образовательными услугами (курсами)"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    ru = RequestUtils()
    ju = JournalService()
    pu = ProfileService()
    pru = ProgramService()
    respu = ResponseUtils()

    queryset = education_service_queryset()
    lookup_field = "object_id"
    serializer_class = EducationServiceListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = EducationServiceFilter

    @swagger_auto_schema(
        tags=['Учебная часть. Образовательные услуги', ],
        operation_description="Получение списка образовательных услуг (курсов)",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': EducationServiceListSerializer(many=True)
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
                    'description': 'Ошибка при получении списка образовательных услуг (курсов)'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Учебная часть. Образовательные услуги', ],
        operation_description="Получение объекта образовательной услуги (курса)",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении объекта',
            '200': EducationServiceRetrieveSerializer
        }
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = EducationServiceRetrieveSerializer(instance)
            return self.respu.ok_response_dict(serializer.data)
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Системная ошибка при получении объекта образовательной услуги'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Учебная часть. Образовательные услуги', ],
        operation_description="Добавление/обновление образовательной услуги (курса)",
        request_body=EducationServiceAddUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при добавлении/обновлении образовательной услуги (курса)',
            '200': 'Сообщение "Образовательная услуга успешно добавлена/обновлена"'
        }
    )
    def create_update(self, request, *args, **kwargs):
        serialize = EducationServiceAddUpdateSerializer(data=request.data)
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
                'edu',
                request
            )
            if process.process_completed:
                return self.respu.ok_response('Образовательная услуга успешно добавлена/обновлена')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            return self.respu.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=['Учебная часть. Образовательные услуги', ],
        operation_description="Удаление образовательной услуги (курса)",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при удалении образовательной услуги (курса)',
            '200': 'Сообщение "бразовательная услуга (курс) успешно удалена"'
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
                'edu',
                request
            )
            if proc.process_completed:
                return self.respu.ok_response('Образовательная услуга (курс) успешно удалена')
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Системная ошибка при удалении образовательной услуги (курса)'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
        return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
