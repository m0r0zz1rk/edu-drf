from django.urls import path

from apps.docs.api.doc_viewer import DovViewerViewSet
from apps.docs.api.student_doc import StudentDocViewSet

urlpatterns = [
    path('student_docs/', StudentDocViewSet.as_view({'get': 'get_student_docs'})),
    path('upload_student_doc/', StudentDocViewSet.as_view({'post': 'create_student_doc'})),
    path('doc_viewer/<str:file_type>/<uuid:file_id>/', DovViewerViewSet.as_view({'get': 'doc_view'})),
    path('rename_peg/', DovViewerViewSet.as_view({'get': 'rename_peg_into_jpeg'})),
]
