from django.urls import path

from apps.commons.drf.routers.LRUE_router import ListRetrieveUpdateExportRouter
from apps.guides.api.profiles.student import StudentProfileViewSet

student_profile_router = ListRetrieveUpdateExportRouter(trailing_slash=True)
student_profile_router.register('student_profile', StudentProfileViewSet)

student_profile_urlpatterns = [
    path('student_profile/check_phone/', StudentProfileViewSet.as_view({'post': 'check_user_phone'})),
    path('student_profile/check_email/', StudentProfileViewSet.as_view({'post': 'check_user_email'})),
    path('student_profile/check_snils/', StudentProfileViewSet.as_view({'post': 'check_user_snils'})),
    path('student_profile/password_change/', StudentProfileViewSet.as_view({'post': 'change_user_password'}))
]

student_profile_urlpatterns += student_profile_router.urls
