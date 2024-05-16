from django.urls import path

from apps.guides.api.user_viewset import UserViewSet

user_urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list'})),
    path('user/<uuid:object_id>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('user/check_phone/', UserViewSet.as_view({'post': 'check_user_phone'})),
    path('user/check_email/', UserViewSet.as_view({'post': 'check_user_email'})),
    path('user/check_snils/', UserViewSet.as_view({'post': 'check_user_snils'})),
    path('user/update/', UserViewSet.as_view({'post': 'update'})),
    path('user/password_change/', UserViewSet.as_view({'post': 'change_user_password'})),
]
