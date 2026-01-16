from django.urls import path

from apps.applications.api.course_application.user import CourseApplicationUserViewSet
from apps.commons.drf.routers.LRCUD_router import ListRetrieveCreateUpdateDeleteRouter

course_application_user_router = ListRetrieveCreateUpdateDeleteRouter(trailing_slash=True)
course_application_user_router.register('course_application_user', CourseApplicationUserViewSet)

course_urls = [
    path('course_application_user/archive/', CourseApplicationUserViewSet.as_view({'get': 'archive_list'})),
    path('course_application_user/payment/<uuid:app_id>/', CourseApplicationUserViewSet.as_view({'get': 'payment'})),
    path('course_application_user/study_url/<uuid:app_id>/', CourseApplicationUserViewSet.as_view({'get': 'study_url'}))
]

course_urls += course_application_user_router.urls
