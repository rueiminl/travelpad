"""
Django settings for webapps project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ConfigParser
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

config = ConfigParser.ConfigParser()
config.read(os.path.join(BASE_DIR, "config.ini"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*q8)kp!a-%b$dvfg+y$s32)##^hwuykp$3hk2e^^q&xd4c1ph8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'travelpad',
    'bootstrap3_datetime',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)

ROOT_URLCONF = 'webapps.urls'
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'

WSGI_APPLICATION = 'webapps.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': config.get('Database', 'Name'),
        'USER': config.get('Database', 'User'),
        'PASSWORD': config.get('Database', 'Password'),
        'HOST': config.get('Database', 'Host'),   # Or an IP Address that your DB is hosted on
        'PORT': config.get('Database', 'Port'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'travelpad/')
#STATIC_ROOT = '/home/ubuntu/team27/travelpad/'

MEDIA_ROOT = os.path.join(BASE_DIR)
#MEDIA_ROOT = '/home/ubuntu/team27/'

MEDIA_URL = '/pictures/'
#STATICFILES_DIRS = (
#    '/var/www/travelpad/travelpad/static',
#)

EMAIL_HOST = config.get('Email', 'Host')
EMAIL_PORT = config.get('Email', 'Port')
EMAIL_HOST_USER = config.get('Email', 'User')
EMAIL_HOST_PASSWORD = config.get('Email', 'Password')
EMAIL_USE_SSL = True
