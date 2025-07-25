from ..settings import env, BASE_DIR, os

SECRET_KEY = env.str('SECRET_KEY')

JWT_ALGORITHM = env.str('JWT_ALGORITHM', 'HS256')

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = env.int('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 15)

AIS_ADDRESS = env.str('AIS_ADDRESS')

RUOREFS_MOSRU_KEY = env.str('RUOREFS_MOSRU_KEY')

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres'
]

REQ_APPS = [
    'corsheaders',
    'django_filters',
    'drf_yasg',
    'import_export',
    'rest_framework',
    'django_rest_passwordreset',
    'tinymce'
]

PROJECT_APPS = [
    'apps.admins',
    'apps.applications',
    'apps.authen',
    'apps.celery_app',
    'apps.commons',
    'apps.docs',
    'apps.edu',
    'apps.guides',
    'apps.journal',
    'apps.reports',
    'apps.surveys',
    'apps.users'
]

INSTALLED_APPS = DJANGO_APPS + REQ_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates/',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'web_app.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Irkutsk'

USE_I18N = True

USE_TZ = True

DATE_INPUT_FORMATS = ['%d.%m.%Y',]

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

CORS_EXPOSE_HEADERS = (
    'Access-Control-Expose-Headers: Content-Disposition, X-Requested-With',
)
