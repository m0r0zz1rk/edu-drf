from django.apps import apps

journal_output_model = apps.get_model('journal', 'JournalOutput')
