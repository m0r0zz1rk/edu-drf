from apps.guides.routers.audience_category import audience_category_router
from apps.guides.routers.profiles.coko import coko_urlpatterns
from apps.guides.routers.event_type import event_type_router
from apps.guides.routers.mo import mo_router
from apps.guides.routers.oo import oo_router
from apps.guides.routers.oo_type import oo_type_router
from apps.guides.routers.position import position_router
from apps.guides.routers.position_category import position_category_router
from apps.guides.routers.region import region_router
from apps.guides.routers.state.state_administrator import state_administrator_router
from apps.guides.routers.state.state_registration import state_registration_router
from apps.guides.routers.profiles.student import student_profile_urlpatterns

urlpatterns = (
    state_registration_router.urls +
    state_administrator_router.urls +
    student_profile_urlpatterns +
    coko_urlpatterns +
    mo_router.urls +
    oo_type_router.urls +
    oo_router.urls +
    audience_category_router.urls +
    event_type_router.urls +
    position_category_router.urls +
    position_router.urls +
    region_router.urls
)
