from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.commons.utils.django.django import DjangoUtils
from .vars.yasg import urlpatterns as yasg_urls

du = DjangoUtils()
static_url = du.get_parameter_from_settings('STATIC_URL')
static_root = du.get_parameter_from_settings('STATIC_ROOT')
media_url = du.get_parameter_from_settings('MEDIA_URL')
media_root = du.get_parameter_from_settings('MEDIA_ROOT')

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/v1/admins/', include('apps.admins.urls')),
    #path('api/v1/applications/', include('apps.applications.urls')),
    #path('api/v1/auth/', include('apps.authen.urls')),
    #path('api/v1/reports/', include('apps.reports.urls')),
    #path('api/v1/users/', include('apps.users.urls')),
    #path('api/v1/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]

urlpatterns += static(static_url, document_root=static_root)
urlpatterns += static(media_url, document_root=media_root)
urlpatterns += yasg_urls
