from apps.guides.routes.audience_category import audience_category_urlpatterns
from apps.guides.routes.coko import coko_urlpatterns
from apps.guides.routes.event_type import event_type_urlpatterns
from apps.guides.routes.mo import mo_urlpatterns
from apps.guides.routes.oo import oo_urlpatterns
from apps.guides.routes.oo_type import oo_type_urlpatterns
from apps.guides.routes.position import position_urlpatterns
from apps.guides.routes.position_category import position_category_urlpatterns
from apps.guides.routes.region import region_urlpatterns
from apps.guides.routes.state.state_administrator import state_administrator_urlpatterns
from apps.guides.routes.state.state_registration import state_registration_urlpatterns
from apps.guides.routes.user import user_urlpatterns

urlpatterns = (
    state_registration_urlpatterns +
    state_administrator_urlpatterns +
    user_urlpatterns +
    coko_urlpatterns +
    mo_urlpatterns +
    oo_type_urlpatterns +
    oo_urlpatterns +
    audience_category_urlpatterns +
    event_type_urlpatterns +
    position_category_urlpatterns +
    position_urlpatterns +
    region_urlpatterns
)
