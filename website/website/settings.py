from djangoappengine.settings_base import *

import os

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'r_-*^w%e6gh(%)j%%%a@oj9(w1%6#2jxx-b26rz6xv0z!6n%3v'

INSTALLED_APPS = (
    'djangoappengine',
    'djangotoolbox',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'booksManiacs',
)

# INSTALLED_APPS = (
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.sites',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     # Uncomment the next line to enable the admin:
#     'django.contrib.admin',
#     # Uncomment the next line to enable admin documentation:
#     # 'django.contrib.admindocs',
#     'booksManiacs',
# )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)

# LOGIN_REDIRECT_URL = '/guestbook/'

# ADMIN_MEDIA_PREFIX = '/media/admin/'
# MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')
# TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

# ROOT_URLCONF = 'urls'
ROOT_URLCONF = 'website.urls'


STATIC_URL = '/static/'


# # List of callables that know how to import templates from various sources.
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# #     'django.template.loaders.eggs.Loader',
# )

# TEMPLATE_CONTEXT_PROCESSORS = (
#     'django.contrib.auth.context_processors.auth',
#     'django.core.context_processors.request',
# )
