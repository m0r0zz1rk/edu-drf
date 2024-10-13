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
from apps.edu.operations.student_group.add import AddStudentGroup
from apps.edu.operations.student_group.delete import DeleteStudentGroup
from apps.edu.operations.student_group.update import UpdateStudentGroup
from apps.edu.selectors.student_group import student_group_queryset, StudentGroupFilter
from apps.edu.serializers.student_group import StudentGroupListSerializer, StudentGroupAddSerializer, \
    StudentGroupUpdateSerializer, StudentGroupServiceTypeSerializer
from apps.edu.services.program import ProgramService
from apps.journal.consts.journal_modules import EDU
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.services.journal import JournalService


class StudentGroupViewSet(viewsets.ModelViewSet):
    """Работа с учебными группами"""
    permission_classes = [IsAuthenticated, IsAdministrators]
    ru = RequestUtils()
    ju = JournalService()
    pu = ProfileService()
    pru = ProgramService()
    respu = ResponseUtils()

    queryset = student_group_queryset()
    lookup_field = "object_id"
    serializer_class = StudentGroupListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = StudentGroupFilter

    @swagger_auto_schema(
        tags=['Учебная часть. Учебные группы', ],
        operation_description="Получение списка учебных групп",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': StudentGroupListSerializer(many=True)
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
                    'description': 'Ошибка при получении списка учебных групп'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Учебная часть. Учебные группы', ],
        operation_description="Получение информации по учебной группы",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении списка',
            '200': StudentGroupListSerializer
        }
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = StudentGroupListSerializer(
                instance
            )
            return self.respu.ok_response_dict(serializer.data)
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Ошибка при получении информации по учебной группе'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Учебная часть. Учебные группы', ],
        operation_description="Получение типа услуги учебной группы",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении типа',
            '200': StudentGroupServiceTypeSerializer
        }
    )
    def get_service_type(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.ou is not None:
                return self.respu.ok_response_dict({'service_type': 'ou'})
            return self.respu.ok_response_dict({'service_type': 'iku'})
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Ошибка при получении типа услуги учебной группы'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Учебная часть. Учебные группы', ],
        operation_description="Добавление учебной группы",
        request_body=StudentGroupAddSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при получении объекта',
            '200': 'Сообщение "Учебная группа успешно добавлена"'
        }
    )
    def create(self, request, *args, **kwargs):
        try:
            serialize = StudentGroupAddSerializer(data=request.data)
            if serialize.is_valid():
                process = AddStudentGroup({
                    'source': self.pu.get_profile_or_info_by_attribute(
                        'django_user_id',
                        request.user.id,
                        'display_name'
                    ),
                    'module': EDU,
                    'process_data': serialize.validated_data
                })
                if process.process_completed:
                    return self.respu.ok_response('Учебная группа успешно добавлена')
                else:
                    return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
            else:
                return self.respu.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Системная ошибка при добавлении учебной группы'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
            return self.respu.bad_request_no_data()

    @swagger_auto_schema(
        tags=['Учебная часть. Учебные группы', ],
        operation_description="Изменение информации по учебной группе",
        request_body=StudentGroupUpdateSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при изменении информации',
            '200': 'Сообщение "Информация успешно обновлена"'
        }
    )
    def update(self, request, *args, **kwargs):
        serialize = StudentGroupUpdateSerializer(
            data=request.data
        )
        if serialize.is_valid():
            process = UpdateStudentGroup({
                'source': self.pu.get_profile_or_info_by_attribute(
                    'django_user_id',
                    request.user.id,
                    'display_name'
                ),
                'module': EDU,
                'process_data': {
                    **request.data,
                    'group_id': self.kwargs['object_id']
                }
            })
            if process.process_completed:
                return self.respu.ok_response('Информация успешно обновлена')
            else:
                return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
        else:
            return self.respu.bad_request_response(f'Ошибка валидации: {repr(serialize.errors)}')

    @swagger_auto_schema(
        tags=['Учебная часть. Учебные группы', ],
        operation_description="Удаление учебной группы",
        responses={
            '403': 'Пользователь не авторизован или не является администратором',
            '400': 'Ошибка при удалении',
            '200': 'Сообщение "Учебная группа успешно удалена"'
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            proc = DeleteStudentGroup({
                'source': self.pu.get_profile_or_info_by_attribute(
                    'django_user_id',
                    request.user.id,
                    'display_name'
                ),
                'module': EDU,
                'process_data': {'group_id': instance.object_id}
            })
            if proc.process_completed:
                return self.respu.ok_response('Учебная группа успешно удалена')
        except Exception:
            self.ju.create_journal_rec(
                {
                    'source': 'Внешний запрос',
                    'module': EDU,
                    'status': ERROR,
                    'description': 'Ошибка при удалении учебной группы'
                },
                '-',
                ExceptionHandling.get_traceback()
            )
        return self.respu.bad_request_response('Произошла ошибка, повторите попытку позже')
