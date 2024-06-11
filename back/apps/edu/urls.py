from apps.edu.url_patterns.calendar_chart import calendar_chart_urlpatterns
from apps.edu.url_patterns.planning_parameter import planning_parameter_urlpatterns
from apps.edu.url_patterns.program import program_urlpatterns
from apps.edu.url_patterns.services.education_service import education_service_urlpatterns

urlpatterns = (program_urlpatterns +
               calendar_chart_urlpatterns +
               planning_parameter_urlpatterns +
               education_service_urlpatterns)
