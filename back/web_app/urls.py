from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.commons.utils.django.settings import settings_utils
from web_app.yasg import urlpatterns as yasg_urls

static_url = settings_utils.get_parameter_from_settings('STATIC_URL')
static_root = settings_utils.get_parameter_from_settings('STATIC_ROOT')
media_url = settings_utils.get_parameter_from_settings('MEDIA_URL')
media_root = settings_utils.get_parameter_from_settings('MEDIA_ROOT')

urlpatterns = [
    path('backend/admin/', admin.site.urls),
    path('backend/api/v1/admins/', include('apps.admins.urls')),
    path('backend/api/v1/applications/', include('apps.applications.urls')),
    path('backend/api/v1/auth/', include('apps.authen.urls')),
    path('backend/api/v1/commons/', include('apps.commons.urls')),
    path('backend/api/v1/docs/', include('apps.docs.urls')),
    path('backend/api/v1/edu/', include('apps.edu.urls')),
    path('backend/api/v1/guides/', include('apps.guides.urls')),
    path('backend/api/v1/journal/', include('apps.journal.urls')),
    path('backend/api/v1/surveys/', include('apps.surveys.urls')),
    path('backend/api/v1/reports/', include('apps.reports.urls')),
    path('backend/api/v1/users/', include('apps.users.urls')),
    path('backend/api/v1/password_reset/', include('django_rest_passwordreset.urls')),
]

urlpatterns += static(static_url, document_root=static_root)
urlpatterns += static(media_url, document_root=media_root)
urlpatterns += yasg_urls
