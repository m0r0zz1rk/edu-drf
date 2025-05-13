from django.urls import path

from apps.reports.api.report_main_viewset import ReportMainViewSet

urlpatterns = [
    path('dpp/', ReportMainViewSet.as_view({'post': 'dpp'})),
    path('service_chart/', ReportMainViewSet.as_view({'post': 'service_chart'})),
    path('pk_one/', ReportMainViewSet.as_view({'post': 'pk_one'})),
    path('fis_frdo/', ReportMainViewSet.as_view({'post': 'fis_frdo'})),
]
