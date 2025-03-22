from apps.applications.api.course_application.admin import CourseApplicationAdminViewSet
from apps.commons.drf.routers.LRUD_router import ListRetrieveUpdateDeleteRouter

course_application_admin_router = ListRetrieveUpdateDeleteRouter(trailing_slash=True)
course_application_admin_router.register('course_application_admin', CourseApplicationAdminViewSet)
