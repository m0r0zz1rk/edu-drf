from django.urls import path

from apps.applications.api.course_certificate import CourseCertificateViewSet
from apps.commons.drf.routers.LRU_router import ListRetrieveUpdateRouter

course_certificate_router = ListRetrieveUpdateRouter(trailing_slash=True)
course_certificate_router.register('course_certificate', CourseCertificateViewSet)

urlpatterns = [
    path('course_certificate/generate/', CourseCertificateViewSet.as_view({'post': 'generate'}))
]

urlpatterns += course_certificate_router.urls
