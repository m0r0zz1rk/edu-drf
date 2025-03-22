from django.apps import apps

from apps.commons.orm.base_orm import BaseORM

# Модель приказов ДПП
program_order_model = apps.get_model('docs', 'ProgramOrder')

# Класс ORM для приказов ДПП
program_order_orm = BaseORM(model=program_order_model)
