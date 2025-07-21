import uuid

from apps.applications.consts.application_statuses import STUDY_COMPLETE
from apps.applications.selectors.course_application import course_application_orm
from apps.applications.selectors.event_application import event_application_orm
from apps.applications.services.course_application import course_application_service
from apps.applications.services.event_application import event_application_service
from apps.surveys.consts.survey_target_types import EDU, INFO
from apps.surveys.selectors.student_answer import student_answer_model
from apps.surveys.services.survey import survey_service
from apps.surveys.services.survey_question import SurveyQuestionService


class StudentAnswerService:
    """Класс методов для работы с ответами обучающихся на вопросы опросов"""

    @staticmethod
    def save_answers(app_id: uuid, answers: list):
        """
        Сохранение ответов обучающихся
        :param app_id: object_id заявки
        :param answers: список с ответами в формате:
            question_id: object_id вопроса
            value: ответ обучающегося
        :return:
        """
        app = course_application_service.get_course_app(app_id)
        orm = course_application_orm
        if not app:
            app = event_application_service.get_event_app(app_id)
            orm = event_application_orm
        group = app.group
        survey_id = survey_service.get_survey_id_for_group(group.object_id)
        sq_service = SurveyQuestionService(survey_id)
        for answer in answers:
            question = sq_service.get_question('object_id', answer.get('question_id'))
            student_answer_model.objects.create(
                survey_id=survey_id,
                group_code=group.code,
                group_type='ПК' if group.ou else INFO,
                question=question.text,
                answer=answer.get('value')
            )
        orm.update_record(
            filter_by=dict(object_id=app_id),
            update_object={'status': STUDY_COMPLETE, 'check_survey': True}
        )


student_answer_service = StudentAnswerService()
