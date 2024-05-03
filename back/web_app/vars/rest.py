from .ldap import *

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.commons.utils.django.auth.auth_backend.AuthBackend',
        'web_app.vars.ldap_classes.LDAPBackend1',
        'web_app.vars.ldap_classes.LDAPBackend2',
    ),
    'DATE_INPUT_FORMATS': ["%d.%m.%Y", ],
    'DATETIME_INPUT_FORMATS': [("%d.%m.%Y %H:%M"), ],
    'DATE_FORMAT': '%d.%m.%Y',
    'DATETIME_FORMAT': '%d.%m.%Y %H:%M',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend',]
}
