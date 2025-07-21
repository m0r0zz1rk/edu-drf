import uuid

from django.db.models import QuerySet

from apps.surveys.exceptions.survey_question_answer import IncorrectAnswerData, AnswerDoesNotExists
from apps.surveys.selectors.survey_question_answer import survey_question_answer_model


class SurveyQuestionAnswerService:
    """Класс методов для работы с возможными ответами вопроса"""

    answer_required_data = [
        'survey_question_id',
        'text'
    ]

    def check_correct_answer_data(self, data: dict) -> bool:
        """
        Проверка на корректные данные об ответе
        :param data: Словарь с данными по ответу вопроса
        :return: True - данные корректны, False - данные не корректны
        """
        for key in self.answer_required_data:
            if key not in data:
                return False
        return True

    @staticmethod
    def get_answers_for_question(question_id: uuid) -> QuerySet:
        """
        Получение возможных вариантов ответов для вопроса
        :param question_id: object_id вопроса
        :return: QuerySet с возможными вариантами ответов
        """
        return survey_question_answer_model.objects.filter(survey_question=question_id)

    def add_edit_answer(self, answer_data):
        """
        Добавление/изменение возможного ответа вопроса
        """
        if not self.check_correct_answer_data(answer_data):
            raise IncorrectAnswerData
        obj_id = None
        if 'object_id' in answer_data:
            obj_id = answer_data['object_id']
            del answer_data['object_id']
        survey_question_answer_model.objects.update_or_create(
            object_id=obj_id,
            defaults=answer_data
        )

    @staticmethod
    def delete_answer(answer_id: uuid):
        """
        Удаление возможного ответа вопроса
        :param answer_id: object_id объекта возможного ответа вопроса
        """
        try:
            survey_question_answer_model.objects.get(object_id=answer_id).delete()
        except Exception:
            raise AnswerDoesNotExists


survey_question_answer_service = SurveyQuestionAnswerService()
