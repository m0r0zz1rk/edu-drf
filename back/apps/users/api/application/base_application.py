from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.utils.django.response import response_utils
from apps.journal.consts.journal_modules import USERS
from apps.journal.consts.journal_rec_statuses import ERROR
from apps.journal.decorators.journal_api import journal_api
from apps.surveys.services.student_answer import student_answer_service
from apps.surveys.services.survey_question import survey_question_service
from apps.users.serializers.survey_answers_serializer import SurveyAnswersSerializer
from apps.users.serializers.survey_questions_serializer import SurveyQuestionsSerializer


class BaseApplicationViewSet(viewsets.ViewSet):
    """Класс эндпоинтов, общих для завок на курсы и мероприятия"""

    @swagger_auto_schema(
        tags=['Обучающиеся. Общее для заявок', ],
        operation_description="Получение списка вопросов опроса",
        responses={
            '403': 'Пользователь не авторизован или не является обучающимся',
            '400': 'Ошибка при получении списка вопросов',
            '200': SurveyQuestionsSerializer(many=True)
        }
    )
    @journal_api(
        USERS,
        ERROR,
        'Ошибка при получении списка вопросов опроса',
        'Произошла ошибка при получении списка вопросов опроса'
    )
    def get_questions(self, request, *args, **kwargs):
        data = survey_question_service.get_questions_for_application(self.kwargs.get('app_id'))
        serialize = SurveyQuestionsSerializer(data, many=True)
        return response_utils.ok_response_list(serialize.data)

    @swagger_auto_schema(
        tags=['Обучающиеся. Общее для заявок', ],
        operation_description="Сохранение ответов на вопросы опроса",
        request_body=SurveyAnswersSerializer,
        responses={
            '403': 'Пользователь не авторизован или не является обучающимся',
            '400': 'Ошибка при сохранении ответов на вопросы',
            '200': 'OK'
        }
    )
    @journal_api(
        USERS,
        ERROR,
        'Ошибка при сохранении ответов на вопросы',
        'Произошла ошибка при сохранении ответов на вопросы'
    )
    def save_answers(self, request, *args, **kwargs):
        serialize = SurveyAnswersSerializer(data=request.data)
        if serialize.is_valid():
            student_answer_service.save_answers(self.kwargs.get('app_id'), request.data.get('data'))
            return response_utils.ok_response('OK')
        else:
            return response_utils.bad_request_response(f'Ошибка сериализации: {repr(serialize.errors)}')

