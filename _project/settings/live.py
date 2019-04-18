import sys
from .base import *

DEBUG = False

INSTALLED_APPS = PROD_APPS

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'testserver',  # needed for django_medusa
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/data/hnhiring.db',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

MEDUSA_DEPLOY_DIR="/data/cache"
