# In production set the environment variable like this:
#    DJANGO_SETTINGS_MODULE=my_proj.settings.production
from .base import *             # NOQA
import logging.config

# For security and performance reasons, DEBUG is turned off
DEBUG = False

# Must mention ALLOWED_HOSTS in production!
ALLOWED_HOSTS = [
    'dinglab-logo.liang2.io',
]


# Cache the templates in memory for speed-up
loaders = [
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]

TEMPLATES[0]['OPTIONS'].update({"loaders": loaders})
TEMPLATES[0]['OPTIONS'].update({"debug": False})
TEMPLATES[0]['APP_DIRS'] = False


# Email settings

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')

DEFAULT_FROM_EMAIL = SERVER_EMAIL = '{name} <{addr}>'.format(
    name=env.str('EMAIL_SENDER_NAME', 'Ding Lab Logo Proposal'),
    addr=env.str('EMAIL_SENDER_ADDRESS'),
)


# Caching
# Ref: https://docs.djangoproject.com/en/1.10/topics/cache/

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'biocloud-localmem',
    }
}


# HTTPS related settings

SECURE_HSTS_SECONDS = 2592000
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
X_FRAME_OPTIONS = 'DENY'


# Log everything to the logs directory at the top
LOGFILE_ROOT = join(dirname(BASE_DIR), 'logs')

# Reset logging
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (
                '[%(asctime)s] %(levelname)s '
                '[%(pathname)s:%(lineno)s] %(message)s'
            ),
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'django_log_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': join(LOGFILE_ROOT, 'django.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django_log_file', ],
            'propagate': True,
            'level': 'INFO',
        },
    }
}

for app in LOCAL_APPS:
    app_handler = '%s_log_file' % app
    app_log_filepath = '%s.log' % app
    LOGGING['loggers'][app] = {
        'handlers': [app_handler, ],
        'level': 'INFO',
    }
    LOGGING['handlers'][app_handler] = {
        'level': 'INFO',
        'class': 'logging.FileHandler',
        'filename': join(LOGFILE_ROOT, app_log_filepath),
        'formatter': 'verbose',
    }

logging.config.dictConfig(LOGGING)
