from django.urls import path

from apps.journal.api.journal import JournalViewSet

urlpatterns = [
    path('journal/', JournalViewSet.as_view({'get': 'list'}))
]
