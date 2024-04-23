from .base import *

REST_FRAMEWORK = {
    #'DEFAULT_AUTHENTICATION_CLASSES': (
    #    'apps.authen.processes.authenticate.AuthBackend',
    #),
    'DATE_INPUT_FORMATS': [("%d.%m.%Y"),],
    'DATETIME_INPUT_FORMATS': [("%d.%m.%Y %H:%M"),],
    'DATE_FORMAT': '%d.%m.%Y',
    'DATETIME_FORMAT': '%d.%m.%Y %H:%M',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend',]
}
