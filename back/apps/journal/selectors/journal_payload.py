from django.apps import apps

journal_payload_model = apps.get_model('journal', 'JournalPayload')
