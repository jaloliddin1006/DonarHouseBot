import os
from pathlib import Path
from environs import Env
from .iiko import *

BASE_DIR = Path(__file__).resolve().parent.parent

if not os.path.exists(os.path.join(BASE_DIR,'.env')):
    print(".env fayli topilmadi!\n\n"
          ".env.example faylidan nusxa ko'chirib shablonni o'zingizga moslang.")
    exit(1)

env = Env()
env.read_env()

API_TOKEN = env.str("API_TOKEN")
SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG")
ADMINS = env.list("ADMINS")

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")

IS_PRODUCTION=env.bool("IS_PRODUCTION")
TELEGRAM_GROUP_ID=-4554019429

if IS_PRODUCTION:
    PAYMENT_TOKEN_CLICK = env.str("PAYMENT_TOKEN_CLICK")
    PAYMENT_TOKEN_PAYMEE = env.str("PAYMENT_TOKEN_PAYMEE")
else:
    PAYMENT_TOKEN_CLICK = env.str("TEST_PAYMENT_TOKEN_CLICK")
    PAYMENT_TOKEN_PAYMEE = env.str("TEST_PAYMENT_TOKEN_PAYMEE")
    

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = [
    "127.0.0.1",
]

TESTING = True
# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    "debug_toolbar",
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mptt',
    'markdownx',
    'tgbot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware", # for debug
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'src.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASE WITH SQLITE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASE WITH POSTGRES
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': DB_NAME,
#         'USER': DB_USER,
#         "PASSWORD": DB_PASS,
#         "HOST": DB_HOST,
#         "PORT": DB_PORT,
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('uz', 'O‘zbekcha'),
    ('ru', 'Русский'),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz' 
MODELTRANSLATION_LANGUAGES = ('uz', 'ru')  
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'uz' 

MODELTRANSLATION_TRANSLATION_FILES = (
    'tgbot.translation',
)

# Tarjima fayllari joylashgan joy
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'tgbot', 'locale'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.alerts.AlertsPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

from src.jazzmin_conf import *

if TESTING:
    JAZZMIN_SETTINGS['show_ui_builder'] = True
else:
    JAZZMIN_SETTINGS['show_ui_builder'] = False
    