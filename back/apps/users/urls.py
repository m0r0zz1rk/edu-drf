from django.urls import path

from apps.users.api.form_data.form_data import FormDataViewSet
from apps.users.api.form_data.oo import FormDataOoViewSet
from apps.users.api.form_data.oo_type import FormDataOoTypeViewSet
from apps.users.api.service import ServicesViewSet
from apps.users.routers.course_application import course_application_router
from apps.users.routers.event_application import event_application_router

urlpatterns = [
    path('courses/', ServicesViewSet.as_view({'get': 'get_courses_list'})),
    path('events/', ServicesViewSet.as_view({'get': 'get_events_list'})),

    path('form_data/', FormDataViewSet.as_view({'get': 'get_form_data'})),
    path('oos/<uuid:mo_id>/', FormDataOoViewSet.as_view({'get': 'list'})),
    path('oo_types/', FormDataOoTypeViewSet.as_view({'get': 'list'})),
]

urlpatterns += course_application_router.urls
urlpatterns += event_application_router.urls
