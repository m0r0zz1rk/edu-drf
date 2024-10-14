from django.urls import path

from apps.applications.api.course_application import CourseApplicationAdminViewSet

urlpatterns = [
    path('course_group_apps/<uuid:group_id>/', CourseApplicationAdminViewSet.as_view({'get': 'list'})),
]
