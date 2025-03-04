import datetime
import environ
import sys

from pathlib import Path


BASE_DIR = Path.cwd()
ASSETS_DIR = BASE_DIR / 'assets'

env = environ.Env(
    DEBUG=(bool, False),
)
env_path = BASE_DIR / '.env'
environ.Env.read_env(str(env_path))


DEBUG = env('DEBUG')

SECRET_KEY = env.str('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
]

INTERNAL_APPS = [
    'app.misc',
    'app.users',
    'app.questions',
]

EXTERNAL_APPS = [
    'rest_framework',
    'drf_yasg',
    'django_dramatiq',
    'debug_toolbar',
]

INSTALLED_APPS = DJANGO_APPS + INTERNAL_APPS + EXTERNAL_APPS

if 'collectstatic' not in sys.argv:
    DATABASES = {
        'default': env.db(),
    }

CACHES = {
    'dummy': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'},
    'locmem': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'},
    'redis': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [env.str('REDIS_URL', 'redis://redis:6379/1')],
        'TIMEOUT': 15 * 60,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
        },
        'KEY_PREFIX': 'udz',
    },
}
CACHES['default'] = CACHES[env.str('DEFAULT_CACHE_BACKEND', 'dummy')]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(BASE_DIR / 'app/templates'),
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'

if 'collectstatic' not in sys.argv:
    DATABASES = {
        'default': env.db()
    }

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'index'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.joinpath('staticfiles')
STATICFILES_DIRS = [
    BASE_DIR.joinpath('static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        #'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'users': '2/minute',
    },
}

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

DRAMATIQ_BROKER = {
    'BROKER': 'dramatiq.brokers.rabbitmq.RabbitmqBroker',
    'OPTIONS': {
        'url': env.str('RABBITMQ_URL', ''),
    },
    'MIDDLEWARE': [
        'dramatiq.middleware.Prometheus',
        'dramatiq.middleware.AgeLimit',
        'dramatiq.middleware.TimeLimit',
        'dramatiq.middleware.Callbacks',
        'dramatiq.middleware.Retries',
        'django_dramatiq.middleware.DbConnectionsMiddleware',
    ]
}

DRAMATIQ_TASKS_DATABASE = 'default'


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: False,
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'  # noqa
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'app': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },
    },
}

RETRAIN_PASSWORD = env.str('RETRAIN_PASSWORD', 'klapaucius')
