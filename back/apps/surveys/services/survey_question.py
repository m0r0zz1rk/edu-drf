import uuid

from apps.applications.services.course_application import course_application_service
from apps.applications.services.event_application import event_application_service
from apps.surveys.consts.survey_question_type import SURVEY_QUESTION_TYPES, ONE, MANY
from apps.surveys.exceptions.survey import SurveyNotExist
from apps.surveys.exceptions.survey_question import IncorrectQuestionInfo, QuestionCreateUpdateError, \
    QuestionDoesNotExist
from apps.surveys.selectors.survey_question import survey_question_model
from apps.surveys.services.survey import survey_service
from apps.surveys.services.survey_question_answer import survey_question_answer_service


class SurveyQuestionService:
    """Класс методов для работы с вопросами опроса"""

    _survey = None

    _survey_question_keys = [
        'sequence_number',
        'question_type',
        'text'
    ]

    def __init__(self, survey_id: uuid = None):
        """
        Получение объекта опроса по полученному object_id опроса
        :param survey_id: object_id опроса
        """
        try:
            self._survey = survey_service.get_survey(
                'object_id',
                survey_id
            )
        except SurveyNotExist:
            pass

    def get_question_count(self) -> int:
        """
        Получение количества вопросов опроса
        :return: количество вопросов
        """
        return survey_question_model.objects.filter(survey_id=self._survey.object_id).count()

    def check_question_exists(self, attribute_name: str, value: str) -> bool:
        """
        Проверка на существующий вопрос опроса
        :param attribute_name: наименование поля модели SurveyQuestion
        :param value: значение атрибута
        :return: True - вопрос найден, False - вопрос отсутствует
        """
        find = {attribute_name: value}
        if self._survey:
            return self._survey.questions.filter(**find).exists()
        return survey_question_model.objects.filter(**find).exists()

    def get_question(self, attribute_name: str, value: str) -> survey_question_model:
        """
        Получение вопроса опроса
        :param attribute_name: наименование поля модели SurveyQuestion
        :param value: значение атрибута
        :return: объект вопроса опроса
        """
        if self.check_question_exists(attribute_name, value):
            find = {attribute_name: value}
            return self._survey.questions.filter(**find).first()
        else:
            raise QuestionDoesNotExist

    def check_and_change_sequence_number(self, start_number: int, seq_number: int):
        """
        Изменение порядковых номеров вопросов опроса в случае совпадения
        полученного номера с одним из номеров вопросов
        """
        if self._survey.questions.filter(sequence_number=seq_number).exists():
            if (self._survey.questions.filter(sequence_number=seq_number + 1).exists() and
                    not seq_number + 1 == start_number):
                self.check_and_change_sequence_number(start_number, seq_number + 1)
            question = self._survey.questions.filter(sequence_number=seq_number).first()
            question.sequence_number = seq_number + 1
            question.save()

    def add_edit_question(self, question_info: dict):
        """
        Добавление или обновление информации о вопросе опроса
        """
        for key in self._survey_question_keys:
            if key not in question_info:
                raise IncorrectQuestionInfo
        try:
            obj_id = None
            if 'object_id' in question_info:
                obj_id = question_info['object_id']
                del question_info['object_id']
                question = self.get_question('object_id', obj_id)
                if question.sequence_number != question_info['sequence_number']:
                    self.check_and_change_sequence_number(
                        question.sequence_number,
                        question_info['sequence_number']
                    )
            else:
                self.check_and_change_sequence_number(
                    question_info['sequence_number'],
                    question_info['sequence_number']
                )
            for question_type in SURVEY_QUESTION_TYPES:
                if question_type[1] == question_info['question_type']:
                    question_info['question_type'] = question_type[0]
            survey_question_model.objects.update_or_create(
                object_id=obj_id,
                defaults=question_info
            )
        except Exception:
            raise QuestionCreateUpdateError

    def delete_question(self, question_id: uuid):
        """
        Удаление вопроса опроса
        :param question_id: object_id вопроса опроса
        """
        if self.check_question_exists('object_id', question_id):
            survey_question_model.objects.filter(object_id=question_id).first().delete()

    @staticmethod
    def get_questions_for_application(app_id: uuid) -> list:
        """
        Получение списка вопросов опроса для заявки обучающегося
        :param app_id: object_id заявки
        :return: список объектов с ключами:
            text - формулировка вопроса
            type - тип вопроса (one, many, short)
            options - список допустимых вариантов ответов (для типа one или many)
        """
        questions = []
        app = course_application_service.get_course_app(app_id)
        if not app:
            app = event_application_service.get_event_app(app_id)
        survey_id = survey_service.get_survey_id_for_group(app.group_id)
        for question in survey_question_model.objects.filter(survey_id=survey_id).order_by('sequence_number'):
            question_options = []
            if question.question_type in [ONE, MANY]:
                question_options = [
                    answer.text for answer in survey_question_answer_service.get_answers_for_question(question.object_id)
                ]
            questions.append({
                'object_id': question.object_id,
                'text': question.text,
                'type': question.question_type,
                'options': question_options
            })
        return questions


survey_question_service = SurveyQuestionService()
