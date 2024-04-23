from .journal import *

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str('EMAIL_HOST', '')
EMAIL_PORT = env.int('EMAIL_PORT', 465)
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', True)
EMAIL_USE_SSL = env.bool('EMAIL_HOST_USER', True)
DEFAULT_FROM_EMAIL = env.str('EMAIL_HOST_USER', '')
SERVER_EMAIL = env.str('EMAIL_HOST_USER', '')
