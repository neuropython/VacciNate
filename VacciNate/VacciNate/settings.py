"""
Django settings for VacciNate project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import environ
from datetime import timedelta
from firebase_admin import initialize_app, credentials
from google.auth import load_credentials_from_file
from celery import Celery
env = environ.Env()
environ.Env.read_env()
from google.auth import credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from django.conf import settings



# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = env('DJANGO_SECRET_KEY')
ENGINE = env("ENGINE")
NAME = env("NAME")
USER = env("USER")
PASSWORD = env("PASSWORD")
HOST = env("HOST")
PORT = env("PORT")
DEBUG_ = env("DJANGO_DEBUG")
REDIS_URL = env("REDIS_URL")

CUSTOM_GOOGLE_APPLICATION_CREDENTIALS = {
  "type": env("type"),
  "project_id": env("project_id"),
  "private_key_id": env("private_key_id"),
  "private_key": env("private_key"),
  "client_email": env("client_email"),
  "client_id": env("client_id"),
  "auth_uri": env("auth_uri"),
  "token_uri": env("token_uri"),
  "auth_provider_x509_cert_url": env("auth_provider_x509_cert_url"),
  "client_x509_cert_url": env("client_x509_cert_url"),
  "universe_domain": env("universe_domain")
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEBUG_

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    # Local apps
    'userapp',
    "vaccinateapp",
    "rest_framework_simplejwt",
    'rest_framework_simplejwt.token_blacklist',
    "push_notifications",
    'fcm_django',
    'django_celery_beat'

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

ROOT_URLCONF = 'VacciNate.urls'

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

WSGI_APPLICATION = 'VacciNate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': ENGINE,
        'NAME': NAME,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '100/day',
        'review-create-throttle': '7/day'
    },
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 2,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    'ROTAATE_REFRESH_TOKENS': True,
}

class CustomFirebaseCredentials(credentials.Credentials):
    def __init__(self):
        super().__init__()
        self._g_credential = None
        self._project_id = None

    def _load_credential(self):
        if not self._g_credential:
            self._g_credential = ServiceAccountCredentials.from_service_account_info(
                settings.CUSTOM_GOOGLE_APPLICATION_CREDENTIALS,
                scopes=credentials._scopes
            )
            self._project_id = settings.CUSTOM_GOOGLE_APPLICATION_CREDENTIALS['project_id']



custom_credentials = CustomFirebaseCredentials(CUSTOM_GOOGLE_APPLICATION_CREDENTIALS)
FIREBASE_MESSAGING_APP = initialize_app(custom_credentials, name='messaging')

FCM_DJANGO_SETTINGS = {
    "DEFAULT_FIREBASE_APP": FIREBASE_MESSAGING_APP,
    "APP_VERBOSE_NAME": "Vaccinate App",
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": False,
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}


CELERY_TIMEZONE = "Europe/Warsaw"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ALWAYS_EAGER = True