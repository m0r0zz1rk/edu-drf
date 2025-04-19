from apps.applications.routers.course_application.admin import urlpatterns as course_urlpatterns
from apps.applications.routers.course_application.user import course_application_user_router
from apps.applications.routers.course_certificate import urlpatterns as certificate_urlpatterns
from apps.applications.routers.event_application.admin import urlpatterns as event_urlpatterns
from apps.applications.routers.event_application.user import event_application_user_router

urlpatterns = (
    course_urlpatterns +
    course_application_user_router.urls +
    event_urlpatterns +
    event_application_user_router.urls +
    certificate_urlpatterns
)
