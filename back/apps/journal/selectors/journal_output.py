from django.apps import apps

# Модель выходных данных записи журнала
journal_output_model = apps.get_model('journal', 'JournalOutput', require_ready=False)
