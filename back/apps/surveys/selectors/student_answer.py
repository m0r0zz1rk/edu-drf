from django.apps import apps

student_answer_model = apps.get_model('surveys', 'StudentAnswer')
