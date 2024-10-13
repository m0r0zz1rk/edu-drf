from django.urls import path

from apps.edu.api.schedule import ScheduleViewSet

schedule_urlpatterns = [
    path('schedule/<uuid:group_id>/', ScheduleViewSet.as_view({'get': 'get_group_schedule'})),
    path('schedule/generate/', ScheduleViewSet.as_view({'post': 'generate_schedule'})),
    path('schedule/save_day/', ScheduleViewSet.as_view({'post': 'save_day_info'}))
]
