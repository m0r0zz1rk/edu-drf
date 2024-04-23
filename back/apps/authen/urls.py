from django.urls import path

from apps.authen.api.authorization_viewset import AuthorizationViewSet
from apps.authen.api.profile_viewset import ProfileViewSet
from apps.authen.api.registration_viewset import RegistrationViewSet
from apps.authen.api.states_viewset import StatesViewSet

authorization_urlpatterns = [
    path('login/', AuthorizationViewSet.as_view({'post': 'user_login'})),
    path('check_auth/', AuthorizationViewSet.as_view({'get': 'check_auth'})),
    path('check_admin/', AuthorizationViewSet.as_view({'get': 'check_admin'}))
]

registration_urlpatterns = [
    path('registration/', RegistrationViewSet.as_view({'post': 'registration'})),
    path('check_email/', RegistrationViewSet.as_view({'post': 'check_unique_email'})),
    path('check_phone/', RegistrationViewSet.as_view({'post': 'check_unique_phone'})),

]

profile_urlpatterns = [
    path('profile/', ProfileViewSet.as_view({'get': 'get_user_information'})),
    path('check_change_email/', ProfileViewSet.as_view({'post': 'check_change_email'})),
    path('check_change_phone/', ProfileViewSet.as_view({'post': 'check_change_phone'})),
    path('change_profile/', ProfileViewSet.as_view({'post': 'save_profile_changes'})),
    path('change_password/', ProfileViewSet.as_view({'post': 'change_user_password'}))
]

states_urlpatterns = [
    path('states/', StatesViewSet.as_view({'get': 'get_states'}))
]

urlpatterns = authorization_urlpatterns + \
              registration_urlpatterns + \
              profile_urlpatterns + \
              states_urlpatterns
