from .swg import *

DEBUG = True

CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*']

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CORS_ALLOWED_ORIGINS = ['http://localhost:8000', 'http://localhost:5173', 'http://127.0.0.1:8000']
