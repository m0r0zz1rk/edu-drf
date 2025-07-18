from django.urls import path

from apps.applications.api.event_application.user import EventApplicationUserViewSet
from apps.commons.drf.routers.LRCU_router import ListRetrieveCreateUpdateRouter

event_application_user_router = ListRetrieveCreateUpdateRouter(trailing_slash=True)
event_application_user_router.register('event_application_user', EventApplicationUserViewSet)

event_urls = [
    path('event_application_user/archive/', EventApplicationUserViewSet.as_view({'get': 'archive_list'})),
    path('event_application_user/payment/<uuid:app_id>/', EventApplicationUserViewSet.as_view({'get': 'payment'})),
    path('course_application_user/study_url/<uuid:app_id>/', EventApplicationUserViewSet.as_view({'get': 'study_url'}))
]

event_urls += event_application_user_router.urls
