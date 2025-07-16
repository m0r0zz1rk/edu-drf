from apps.applications.routers.course_application.admin import urlpatterns as course_urlpatterns
from apps.applications.routers.course_application.user import course_urls
from apps.applications.routers.course_certificate import urlpatterns as certificate_urlpatterns
from apps.applications.routers.event_application.admin import urlpatterns as event_urlpatterns
from apps.applications.routers.event_application.user import event_urls

urlpatterns = (
    course_urlpatterns +
    course_urls +
    event_urlpatterns +
    event_urls +
    certificate_urlpatterns
)
