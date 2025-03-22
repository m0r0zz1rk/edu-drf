from apps.commons.drf.routers.LRCUD_router import (
    ListRetrieveCreateUpdateDeleteRouter)
from apps.users.api.application.course_application import CourseApplicationViewSet

course_application_router = ListRetrieveCreateUpdateDeleteRouter(trailing_slash=True)
course_application_router.register('course_application', CourseApplicationViewSet)
