"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from prettyconf import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    'SECRET_KEY',
    default="Don't forget to set this in a .env file."
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=config.boolean, default=True)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    cast=config.list,
    default='localhost, 127.0.0.1',
)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_extensions',
    'django_rq',
    'colorfield',
    'leaflet',
    'import_export',
    'commons',
    'homepage',
    'events',
    'locations',
    'organizations',
    'schedule',
    'speakers',
    'tickets',
    'invoices',
    'api',
    'certificates',
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

ROOT_URLCONF = 'main.urls'

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
                'commons.context_processors.glob'
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config(
            'DATABASE_ENGINE',
            default='django.db.backends.postgresql'
        ),
        'NAME': config('DATABASE_NAME', default='pythoncanarias'),
        'USER': config('DATABASE_USER', default='pythoncanarias'),
        'PASSWORD': config('DATABASE_PASSWORD', default='pythoncanarias'),
        'HOST': config('DATABASE_HOST', default='127.0.0.1')
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': ('django.contrib.auth.password_validation.UserAttributeSimilarityValidator')},
    {'NAME': ('django.contrib.auth.password_validation.MinimumLengthValidator')},
    {'NAME': ('django.contrib.auth.password_validation.CommonPasswordValidator')},
    {'NAME': ('django.contrib.auth.password_validation.NumericPasswordValidator')},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = config('TIME_ZONE', default='UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = config('STATIC_ROOT', default=os.path.join(BASE_DIR, ".static"))
MEDIA_ROOT = config('MEDIA_ROOT', default=os.path.join(BASE_DIR, ".media"))

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

SITE_ID = 1

# Python Canarias Info
#
# You probably want to change this to use this code

ASSOCIATION_NAME = config('ASSOCIATION_NAME', default='Python Canarias')
DOMAIN = config('DOMAIN', default='pythoncanarias.es')
CONTACT_EMAIL = config('CONTACT_EMAIL', default='info@{}'.format(DOMAIN))


# Leaflet settings

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (28.4818, -16.3206),
    'DEFAULT_ZOOM': 16,
    'MIN_ZOOM': 5,
    'MAX_ZOOM': 19,
    'RESET_VIEW': False,
}


# Stripe settings

STRIPE_PUBLIC_KEY = config(
    'STRIPE_PUBLIC_KEY',
    default='Set your Stripe api public key in .env file',
)

STRIPE_SECRET_KEY = config(
    'STRIPE_SECRET_KEY',
    default='Set your Stripe api secret key in .env file',
)

LOAD_FONTS_IN_REPORTS = config(
    'LOAD_FONTS_IN_REPORTS',
    default=True,
    cast=config.boolean
)

SENDGRID_API_KEY = config('SENDGRID_API_KEY', default='<sengrid api key>')


LOGFILE_NAME = os.path.join(BASE_DIR, "web.log")
LOGFILE_SIZE = 1 * 1024 * 1024
LOGFILE_COUNT = 3

LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s \
%(process)d %(thread)d %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
    "handlers": {
        # Log to console
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
        },
        # Log to a text file that can be rotated by logrotate
        "logfile": {
            "level": "ERROR",
            "formatter": "verbose",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGFILE_NAME,
            "maxBytes": LOGFILE_SIZE,
            "backupCount": LOGFILE_COUNT,
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "tickets": {
            "handlers": ["logfile", "console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "invoices": {
            "handlers": ["logfile", "console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "events": {
            "handlers": ["logfile", "console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "django": {
            "handlers": ["logfile"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

LC_TIME_SPANISH_LOCALE = config('LC_TIME_SPANISH_LOCALE', default='es_ES.utf8')


RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    }
}

CURRENT_API_VERSION = 1

# invoices
ORG_DATA = {
    'name': config('ORG_NAME', default='Python Canarias'),
    'cif': config('ORG_CIF', default='XXXXXXXXB'),
    'address': config('ORG_ADDRESS', default='Ctra This tthat'),
    'rest_address': config('ORG_REST_ADDRESS', default='peras al limón'),
    'po_box': config('ORG_PO_BOX', default='38023'),
    'city': config('ORG_CITY', default='San Cristobal de La Laguna'),
    'email': config('ORG_EMAIL', default='info@pythoncanarias.es'),
    'web': config('ORG_WEB', default='www.pythoncanarias.es'),
    'iban': config('ORG_IBAN', default='111222333'),
}
