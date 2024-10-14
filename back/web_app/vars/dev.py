from .swg import *

DEBUG = True

CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*']

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': env.str('DEV_DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': env.str('DEV_DB_NAME', 'db.sqlite3'),
        'USER': env.str('DEV_DB_USER', ''),
        'PASSWORD': env.str('DEV_DB_PASSWORD', ''),
        'HOST': env.str('DEV_DB_HOST', ''),
        'PORT': env.str('DEV_DB_PORT', ''),
        'ATOMIC_REQUEST': True,
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'connect_timeout': 120,
        }
    }
}

MEDIA_ROOT = env.str('DEV_MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))

MEDIA_ROOT_OLD = env.str('DEV_MEDIA_ROOT_OLD', os.path.join(BASE_DIR, 'media'))

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:5173',
    'http://127.0.0.1:8000',
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]

CORS_EXPOSE_HEADERS = [
    ''
]
