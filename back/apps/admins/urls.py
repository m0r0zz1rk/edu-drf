from django.urls import path

from apps.admins.api.main_page_viewset import MainPageViewSet

main_page_urlpatterns = [
    path('main_page_info/', MainPageViewSet.as_view({'get': 'get_main_page_centre'})),
]

urlpatterns = main_page_urlpatterns
