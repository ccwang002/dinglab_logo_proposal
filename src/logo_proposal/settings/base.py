"""
Django settings for logo_proposal project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

from datetime import datetime
from os.path import abspath, dirname, join, exists
from pathlib import Path
from django.core.urlresolvers import reverse_lazy
import pytz

# Build paths inside the project like this: join(BASE_DIR, "directory")
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))

# Use 12factor inspired environment variables or from a file
# Powered by django-environ
import environ
env = environ.Env()

# Ideally move env file should be outside the git repo
# i.e. BASE_DIR.parent.parent
env_file = join(dirname(__file__), 'local.env')
if exists(env_file):
    environ.Env.read_env(str(env_file))

# SECURITY WARNING: keep the secret key used in production secret!
# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in
    # os.environ
    'default': env.db()
}


# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'crispy_forms',
    'compressor',
)

LOCAL_APPS = (
    'core',
    'users',
    'proposals',
    'reviews',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'logo_proposal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(BASE_DIR, 'templates'),
            # More template dirs here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
        },
    },
]

WSGI_APPLICATION = 'logo_proposal.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',    # noqa
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',   # noqa
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
#     },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = join(BASE_DIR, 'assets')

STATICFILES_DIRS = [join(BASE_DIR, 'static')]

# list of finder classes that know how to find static files in
# various locations
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)


# Media files settings (user uploaded data)
# https://docs.djangoproject.com/en/1.10/topics/files/

MEDIA_URL = '/media/'

MEDIA_ROOT = env.str('MEDIA_ROOT', str(Path(BASE_DIR, 'media')))


# URL settings.

LOGIN_URL = reverse_lazy('login')

LOGOUT_URL = reverse_lazy('logout')

LOGIN_REDIRECT_URL = reverse_lazy('index')


# Custom user model

AUTH_USER_MODEL = 'users.EmailUser'


# Third-party app and custom settings

LIBSASS_SOURCEMAPS = True

LIBSASS_PRECISION = 10

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

WERKZEUG_DEBUG = env.bool('WERKZEUG_DEBUG', default=False)


# Proposal related settings

NUM_PROPOSALS_PER_USER = 3

NUM_REVIEWS_PER_USER = 5

DATE_DISPLAY_REVIEW_STAT = pytz.UTC.localize(datetime(2016, 9, 30, 17, 0))
