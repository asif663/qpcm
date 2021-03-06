# Django settings for qpcm project.
from __future__ import absolute_import
import sys
import os
from celery.schedules import crontab

import djcelery
path = '/home/chinna/Desktop/Django-1.4/qpcm/qpcmms'
if path not in sys.path:
   sys.path.append(path)

djcelery.setup_loader()

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

#Broker_Settings

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = 'guest'
BROKER_VHOST = "/"

CELERY_IMPORTS = ("qpcmms.tasks")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'qpcm',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Calcutta'

# CELERYBEAT_SCHEDULE = {
#         'add-every-30-seconds': {
#         'task': 'qpcmms.tasks.scraper_example',
#         'schedule': crontab(),
#         'args': ()
#     },
# }

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
# USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# MEDIA_ROOT = ''

path = os.path.abspath('..')

# print os.path.abspath('..')+ '/qpcm/qpcmms/static/qpmedia/'

MEDIA_ROOT = path + '/qpcm/qpcmms/static/qpmedia/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
# MEDIA_URL = ''
MEDIA_URL = 'http://localhost:8000/static/qpmedia/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

IMAGE_ROOT = path + '/qpcm/qpcmms/static/img/'

IMAGE_URL = 'http://localhost:8000/static/img/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '(&amp;=lnap*rkecn*8%p%a@a3%_c)!4(p9*t=ha*)m(%airhh^a+m'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'    

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'qpcm.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'qpcm.wsgi.application'

SESSION_COOKIE_AGE = 12000000

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.abspath(os.path.join(os.path.dirname(__file__),".."))+'\\templates'
    # '/home/chinna/Desktop/Django-1.4/qpcm/templates'
    # os.getcwd()+'/templates'
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'qpcmms',
    'djcelery',
    # 'django_ses'
    # 'south',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# AWS_ACCESS_KEY_ID = 'AKIAI32AAPUWIZRUIR2A'
# AWS_SECRET_ACCESS_KEY = 'Ap+HQbURM8h1WSqhAFO7EslUmS3HAt1mvZielAz/lvoj'
# EMAIL_BACKEND = 'django_ses.SESBackend'

EMAIL_USE_TLS = True 
EMAIL_HOST = 'smtpan.qpgc.net'
EMAIL_PORT = '25'

# CONFIRM_MOBILE = '08978028038' 

# EMAIL_HOST_USER = 'venugopal@anipr.in'
# EMAIL_HOST_PASSWORD = '8885662223chinna'

EMAIL_HOST_USER = 'ladika@qp.com.qa'
EMAIL_HOST_PASSWORD = 'Nasren!!!2'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    #'django.contrib.auth.hashers.BCryptPasswordHasher',
    #'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)