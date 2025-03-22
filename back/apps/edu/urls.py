from apps.edu.url_patterns.calendar_chart import calendar_chart_urlpatterns
from apps.edu.url_patterns.planning_parameter import planning_parameter_urlpatterns
from apps.edu.url_patterns.program import program_urlpatterns
from apps.edu.url_patterns.schedule import schedule_urlpatterns
from apps.edu.url_patterns.services.education_service import education_service_router
from apps.edu.url_patterns.services.information_service import information_service_router
from apps.edu.url_patterns.student_group import student_group_urlpatterns
from apps.edu.url_patterns.teacher import teacher_urlpatterns

urlpatterns = (program_urlpatterns +
               calendar_chart_urlpatterns +
               planning_parameter_urlpatterns +
               education_service_router.urls +
               information_service_router.urls +
               student_group_urlpatterns +
               schedule_urlpatterns +
               teacher_urlpatterns)
