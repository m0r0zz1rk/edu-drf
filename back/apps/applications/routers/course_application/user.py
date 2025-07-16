from django.urls import path

from apps.applications.api.course_application.user import CourseApplicationUserViewSet
from apps.commons.drf.routers.LRCU_router import ListRetrieveCreateUpdateRouter

course_application_user_router = ListRetrieveCreateUpdateRouter(trailing_slash=True)
course_application_user_router.register('course_application_user', CourseApplicationUserViewSet)

course_urls = [
    path('course_application_user/archive/', CourseApplicationUserViewSet.as_view({'get': 'archive_list'})),
]

course_urls += course_application_user_router.urls
