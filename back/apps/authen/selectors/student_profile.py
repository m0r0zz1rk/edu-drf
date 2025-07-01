from django.apps import apps

from apps.commons.orm.base_orm import BaseORM

student_profile_model = apps.get_model('authen', 'StudentProfile')

student_profile_orm = BaseORM(
    model=student_profile_model,
    select_related=['django_user', 'state']
)
