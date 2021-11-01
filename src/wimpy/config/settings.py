from datetime import timedelta
from pathlib import Path

from decouple import Csv, config

from wimpy import __version__, constants

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='changeme')

DEBUG = config('DJANGO_DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default='localhost')


# Application

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'wimpy.healthcheck',
    'wimpy.events',
    # 3rd party apps
    'django_filters',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wimpy.config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'wimpy.config.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
            '%(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'root': {
        'level': config('ROOT_LOG_LEVEL', default='INFO'),
        'handlers': ['console']
    },
    'django': {
        'level': config('DJANGO_LOG_LEVEL', default='INFO'),
        'handlers': ['console']
    },
    'wimpy': {
        'level': config('WIMPY_LOG_LEVEL', default='INFO'),
        'handlers': ['console']
    },
}


# Storage

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    'default': {
        'BACKEND': config(
            'DEFAULT_CACHE_BACKEND',
            default='django.core.cache.backends.dummy.DummyCache'
        ),
        'LOCATION': config(
            'DEFAULT_CACHE_LOCATION',
            default=''
        ),
        'OPTIONS': {
            'TIMEOUT': config(
                'DEFAULT_CACHE_TIMEOUT',
                cast=float,
                default=2
            )
        }
    }
}


# Security

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # NOQA
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # NOQA
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # NOQA
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # NOQA
    },
]


# Local apps

EVENT_DATA_SCHEMA_CACHE_TTL = config(
    'EVENT_DATA_SCHEMA_CACHE_TTL',
    cast=float,
    default=1 * constants.HOURS
)


# 3rd party apps

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.LimitOffsetPagination'
    ),
    'PAGE_SIZE': config('DEFAULT_API_PAGE_SIZE', cast=int, default=50),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        seconds=config(
            'ACCESS_TOKEN_LIFETIME',
            default=2 * constants.HOURS,
            cast=int
        )
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        seconds=config(
            'REFRESH_TOKEN_LIFETIME',
            default=1 * constants.DAYS,
            cast=int
        )
    ),
    'ROTATE_REFRESH_TOKENS': config(
        'ROTATE_REFRESH_TOKENS',
        default=False,
        cast=bool
    ),
    'BLACKLIST_AFTER_ROTATION': config(
        'BLACKLIST_AFTER_ROTATION',
        default=False,
        cast=bool
    ),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Wimpy API',
    'DESCRIPTION': 'Events tracking application',
    'VERSION': __version__,
}


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Assets

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR.parent / 'staticfiles')
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
