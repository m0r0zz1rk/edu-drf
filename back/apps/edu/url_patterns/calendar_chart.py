from django.urls import path

from apps.edu.api.calendar_chapter import CalendarChartViewSet

calendar_chart_urlpatterns = [
    path('kug/<uuid:program_id>/', CalendarChartViewSet.as_view({'get': 'get_kug'})),
    path('kug_update/', CalendarChartViewSet.as_view({'post': 'update_kug'}))
]
