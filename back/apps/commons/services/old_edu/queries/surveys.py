from django.contrib.auth.models import User
from sqlalchemy import text

from apps.commons.services.old_edu.db.db_engine import old_edu_connect_engine
from apps.surveys.consts.survey_question_type import SHORT, ONE, MANY
from apps.surveys.selectors.student_answer import student_answer_model
from apps.surveys.selectors.survey import survey_model
from apps.surveys.selectors.survey_question import survey_question_model


class SurveysData:
    """
    Класс методов для получения и сохранения данных приложения
    Опросы из олдовой базы edu
    """

    question_type_mapping = {
        'Краткий ответ': SHORT,
        'Один ответ': ONE,
        'Несколько ответов': MANY
    }

    @staticmethod
    def get_surveys():
        """
        Получение опросов
        """
        exists = (survey_model.objects.
                  select_related('creator').
                  all())
        users = User.objects.all()
        with old_edu_connect_engine.connect() as conn:
            sql = ('SELECT survey.[id], survey.[description], prof.[user_id] FROM [edu-new].[dbo].[centre_surveys] '
                   'as survey inner join [edu-new].[dbo].[authen_profiles] as prof '
                   'on survey.[creator_id] = prof.[id]')
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for surv in data:
            if len(list(filter(lambda survey: survey.old_id == surv[0], exists))) > 0:
                continue
            try:
                user_id = list(filter(lambda user: user.id == surv[2], users))[0].id
            except Exception:
                print(f'profile - {surv[2]}')
                continue
            new_survey = {
                'old_id': surv[0],
                'creator_id': user_id,
                'description': surv[1]
            }
            survey_model.objects.update_or_create(
                **new_survey
            )
            print(f'Опрос "{new_survey["description"]}" - добавлено')

    def get_survey_questions(self):
        """
        Получение вопросов опросов
        """
        exists = (survey_question_model.objects.
                  select_related('survey').
                  all())
        surveys = (survey_model.objects.
                   select_related('creator').
                   all())
        with old_edu_connect_engine.connect() as conn:
            sql = ('SELECT * '
                   'FROM [edu-new].[dbo].[centre_survquestions]')
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for question in data:
            if len(list(filter(lambda quest: quest.old_id == question[0], exists))) > 0:
                continue
            try:
                survey = list(filter(lambda surv: surv.old_id == question[4], surveys))[0]
            except Exception:
                print(f'survey - {question[4]}')
                continue
            new_survey_question = {
                'old_id': question[0],
                'survey_id': survey.object_id,
                'sequence_number': question[1],
                'question_type': self.question_type_mapping[question[3]],
                'text': question[2]
            }
            survey_question_model.objects.update_or_create(
                **new_survey_question
            )
            print(f'Вопрос "{new_survey_question["text"]} для опроса '
                  f'"{survey.description}" - добавлено')

    def get_student_answers(self):
        """
        Получение ответов обучающихся на вопросы опросов
        """
        exists = (student_answer_model.objects.
                  select_related('survey').
                  all())
        surveys = (survey_model.objects.
                   select_related('creator').
                   all())
        with old_edu_connect_engine.connect() as conn:
            sql = ('SELECT * '
                   'FROM [edu-new].[dbo].[centre_surveysrecords]')
            data_query = conn.execute(text(sql))
            data = data_query.all()
        for answer in data:
            if len(list(filter(lambda ans: ans.old_id == answer[0], exists))) > 0:
                continue
            try:
                survey = list(filter(lambda surv: surv.description == answer[2][:-8], surveys))[0]
            except Exception:
                print(f'survey - {answer[2]}')
                continue
            new_student_answer = {
                'old_id': answer[0],
                'survey_id': survey.object_id,
                'group_code': answer[3],
                'group_type': answer[4],
                'question': answer[5],
                'answer': answer[6]
            }
            student_answer_model.objects.update_or_create(
                **new_student_answer
            )
            print(f'Ответ к опросу "{survey.description}" - добавлено')


