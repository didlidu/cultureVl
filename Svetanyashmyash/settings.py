# coding: utf-8
import os
import sys
from os.path import abspath, dirname


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_PATH = abspath(dirname(__file__))
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'  # URL для медии в шаблонах
STATIC_PATH = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (STATIC_PATH, )
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.MemoryFileUploadHandler",
                        "django.core.files.uploadhandler.TemporaryFileUploadHandler",)

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
TEMPLATE_DIRS = (TEMPLATE_PATH,)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hjxpk*p)pyi*d0gfq(30xon6l1-y8-#hudksp38y4usig1=9&2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'culturevl@yandex.ru'
EMAIL_HOST_PASSWORD = 'Pasha123lol'
DEFAULT_FROM_EMAIL = 'culturevl@yandex.ru'
DEFAULT_TO_EMAIL = 'culturevl@yandex.ru'
SERVER_EMAIL = 'culturevl@yandex.ru'

ADMINS = (('Pavel Mesenev', 'ox1omon@gmail.com'), ('Pavel Mesenev', 'heredemonsnearby@mail.ru'))


ALLOWED_HOSTS = [
    '.culturevl.tk',  # Allow domain and subdomains
    '.culturevl.ru',  # Allow domain and subdomains
    '127.0.0.1',
    '54.149.166.96',
]

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog_app',
    'gunicorn',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'Svetanyashmyash.urls'
WSGI_APPLICATION = 'Svetanyashmyash.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'ru-ru'
LOGIN_URL = '/restricted/login/'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
