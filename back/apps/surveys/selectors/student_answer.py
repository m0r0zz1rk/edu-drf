from django.apps import apps

from apps.commons.orm.base_orm import BaseORM

student_answer_model = apps.get_model('surveys', 'StudentAnswer')

# Класс ORM для работы с ответами обучающихся
student_answer_orm = BaseORM(
    model=student_answer_model,
    select_related=['survey']
)
