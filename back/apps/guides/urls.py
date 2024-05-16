from apps.guides.url_patterns.audience_category_urlpatterns import audience_category_urlpatterns
from apps.guides.url_patterns.coko_urlpatterns import coko_urlpatterns
from apps.guides.url_patterns.event_type_urlpatterns import event_type_urlpatterns
from apps.guides.url_patterns.mo_urlpatterns import mo_urlpatterns
from apps.guides.url_patterns.oo_type_urlpatterns import oo_type_urlpatterns
from apps.guides.url_patterns.oo_urlpatterns import oo_urlpatterns
from apps.guides.url_patterns.position_category_urlpatterns import position_category_urlpatterns
from apps.guides.url_patterns.position_urlpatterns import position_urlpatterns
from apps.guides.url_patterns.state.state_administrator_urlpatterns import state_administrator_urlpatterns
from apps.guides.url_patterns.state.state_registration_urlpatterns import state_registration_urlpatterns
from apps.guides.url_patterns.user_urlpatterns import user_urlpatterns

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
        position_urlpatterns
)
