from django.apps import apps

from apps.commons.orm.base_orm import BaseORM

# Модель договоров оферт
student_group_offer_model = apps.get_model('docs', 'StudentGroupOffer')

# Класс ORM для договоров оферт
student_group_offer_orm = BaseORM(
    model=student_group_offer_model,
    select_related=['group', ]
)
