from django.urls import path

from apps.guides.api.coko_viewset import CokoViewSet
from apps.guides.api.state.state_registration_viewset import StateRegistrationViewSet
from apps.guides.api.user_viewset import UserViewSet

state_urlpatterns = [
    path('states/', StateRegistrationViewSet.as_view({'get': 'list'}))
]

user_urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list'})),
    path('user/<uuid:object_id>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('user/check_phone/', UserViewSet.as_view({'post': 'check_user_phone'})),
    path('user/check_email/', UserViewSet.as_view({'post': 'check_user_email'})),
    path('user/check_snils/', UserViewSet.as_view({'post': 'check_user_snils'})),
    path('user/update/', UserViewSet.as_view({'post': 'update'})),
    path('user/password_change/', UserViewSet.as_view({'post': 'change_user_password'})),
]

coko_urlpatterns = [
    path('cokos/', CokoViewSet.as_view({'get': 'list'})),
    path('coko/change_curator_groups/', CokoViewSet.as_view({'post': 'change_curator_groups'})),
]

urlpatterns = state_urlpatterns + user_urlpatterns + coko_urlpatterns

