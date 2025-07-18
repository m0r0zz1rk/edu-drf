from django.urls import path

from apps.docs.api.doc_viewer import DovViewerViewSet
from apps.docs.api.pay_doc import PayDocViewSet
from apps.docs.api.student_doc import StudentDocViewSet
from apps.docs.api.student_group_docs import StudentGroupDocsViewSet

urlpatterns = [
    path('student_docs/', StudentDocViewSet.as_view({'get': 'get_student_docs'})),
    path('upload_student_doc/', StudentDocViewSet.as_view({'post': 'create_student_doc'})),
    path('doc_viewer/<str:file_type>/<uuid:file_id>/', DovViewerViewSet.as_view({'get': 'doc_view'})),
    path('group_offer/<uuid:group_id>/', StudentGroupDocsViewSet.as_view({'patch': 'partial_update'})),
    path('print_file/', StudentGroupDocsViewSet.as_view({'post': 'print_file'})),
    path('upload_license/', StudentGroupDocsViewSet.as_view({'post': 'upload_licenses'})),

    path('pay_doc/create/', PayDocViewSet.as_view({'post': 'create'}))
]
