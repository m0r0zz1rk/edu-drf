from django.urls import path

from apps.applications.api.course_application.admin import CourseApplicationAdminViewSet
from apps.commons.drf.routers.LRUD_router import ListRetrieveUpdateDeleteRouter

course_application_admin_router = ListRetrieveUpdateDeleteRouter(trailing_slash=True)
course_application_admin_router.register('course_application_admin', CourseApplicationAdminViewSet)

urlpatterns = [
    path('course_pay_denied/<uuid:object_id>/', CourseApplicationAdminViewSet.as_view({'post': 'pay_denied'})),
    path('course_select_move/', CourseApplicationAdminViewSet.as_view({'post': 'select_move'})),
    path('course_all_move/', CourseApplicationAdminViewSet.as_view({'post': 'all_move'})),
    path('course_remove_apps/', CourseApplicationAdminViewSet.as_view({'delete': 'bulk_destroy'}))
]

urlpatterns += course_application_admin_router.urls
