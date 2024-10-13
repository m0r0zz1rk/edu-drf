from django.urls import path

from apps.docs.api.student_doc import StudentDocViewSet

urlpatterns = [
    path('student_docs/', StudentDocViewSet.as_view({'get': 'get_student_docs'})),
    path('upload_student_doc/', StudentDocViewSet.as_view({'post': 'create_student_doc'}))
]
