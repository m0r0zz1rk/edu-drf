from django.apps import apps

from apps.commons.orm.base_orm import BaseORM

# Модель выходных данных записи журнала
journal_output_model = apps.get_model('journal', 'JournalOutput')

# Класс ORM для выходных данных записи журнала
journal_output_orm = BaseORM(model=journal_output_model)
