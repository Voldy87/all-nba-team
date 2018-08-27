"""
Django settings for all_nba_team project.

Generated by 'django-admin startproject' using Django 1.11.12.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import django_heroku

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_o8=a90k47&xtfn#m5)qgcoe9jbpq6k#9rtg&3^_p6=!-@(4t!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'polls.apps.PollsConfig', # audience audit about the site
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', #django-rest-framework (for the private and public API)
    'api',
    'record_pages',
    'splashome', # voldy87 & site-specific splash, home page
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', #i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'all_nba_team.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'all_nba_team/templates',
            'record_pages/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n', #i18n
                #'app.apptemplates.load_setting',
            ],
            'libraries':{
               # 'i18n_include': 'record_pages.templatetags.i18n_include',
            }
        },
    },
]

WSGI_APPLICATION = 'all_nba_team.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': { #heroku-provisioned db (django stuff, polls)
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd4s8j5s205po7t',
        'USER': 'zyqgdtpsbttnxn',
        'PASSWORD': '28e93dff8395329a9c0760a9ad084bae4e028646af7ad5eec2b24c53f9f65046',
        'HOST': 'ec2-54-227-250-33.compute-1.amazonaws.com',
        'PORT': '5432',
    },
    'data': { # private do server (allnba data)
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'all_nba_team',
        'USER': 'postgres',
        'PASSWORD': 'massaciuccoli',
        'HOST': '46.101.238.71',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('de', 'Deutsch'),
    ('en', 'English'),
    ('es', 'Español'),
    ('fr', 'Français'),
    ('it', 'Italiano'),
]
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'record_pages/static'),
    os.path.join(BASE_DIR, 'polls/static'),
) # where to look for static files that are not tied to a particular app.

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') #for the collectstatic command

django_heroku.settings(locals())