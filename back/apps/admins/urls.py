from django.urls import path

from apps.admins.api.main_page import MainPageViewSet
from apps.admins.api.personal_schedule import PersonalScheduleViewSet

main_page_urlpatterns = [
    path('main_page_info/', MainPageViewSet.as_view(
        {'get': 'get_main_page_centre'}
    )),
    path('personal_schedule/', PersonalScheduleViewSet.as_view(
        {'get': 'get_personal_schedule'}
    ))
]

urlpatterns = main_page_urlpatterns
