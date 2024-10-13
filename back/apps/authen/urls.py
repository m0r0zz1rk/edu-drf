from django.urls import path

from apps.authen.api.authorization import AuthorizationViewSet
from apps.authen.api.registration import RegistrationViewSet

from apps.authen.api.profile import ProfileViewSet

authorization_urlpatterns = [
    path('login/', AuthorizationViewSet.as_view({'post': 'user_login'})),
    path('check_auth/', AuthorizationViewSet.as_view({'get': 'check_auth'})),
    path('get_user_role/', AuthorizationViewSet.as_view({'get': 'get_user_role'}))
]

registration_urlpatterns = [
    path('registration/', RegistrationViewSet.as_view({'post': 'registration'})),
    path('check_email/', RegistrationViewSet.as_view({'post': 'check_unique_email'})),
    path('check_phone/', RegistrationViewSet.as_view({'post': 'check_unique_phone'})),
    path('check_snils/', RegistrationViewSet.as_view({'post': 'check_unique_snils'})),
]

profile_urlpatterns = [
    path('student_main_page_info/', ProfileViewSet.as_view({'get': 'get_main_page_student'})),
    path('get_profile/', ProfileViewSet.as_view({'get': 'get_profile_info'})),
    path('save_profile/', ProfileViewSet.as_view({'post': 'save_profile_info'})),
    path('check_profile_email/', ProfileViewSet.as_view({'post': 'check_profile_email'})),
    path('check_profile_phone/', ProfileViewSet.as_view({'post': 'check_profile_phone'})),
    path('check_profile_snils/', ProfileViewSet.as_view({'post': 'check_profile_snils'})),
    path('change_password/', ProfileViewSet.as_view({'post': 'change_user_password'}))
]

urlpatterns = (
    authorization_urlpatterns +
    registration_urlpatterns +
    profile_urlpatterns
)
