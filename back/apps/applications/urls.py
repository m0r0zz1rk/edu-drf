from apps.applications.routers.course_application.admin import course_application_admin_router
from apps.applications.routers.course_application.user import course_application_user_router
from apps.applications.routers.event_application.admin import event_application_admin_router

urlpatterns = (
    course_application_admin_router.urls +
    course_application_user_router.urls +
    event_application_admin_router.urls
)
