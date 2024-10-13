from django.urls import path

from apps.edu.api.teacher import TeacherViewSet

teacher_urlpatterns = [
    path('teachers/', TeacherViewSet.as_view({'get': 'list'})),
    path('teacher_busy/', TeacherViewSet.as_view({'post': 'check_teacher_busy'}))
]
