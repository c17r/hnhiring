import os
import sys

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

DEBUG = False

INSTALLED_APPS = PROD_APPS

ALLOWED_HOSTS = [
    'hnhiring.c17r.com',
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

sentry_sdk.init(
    dsn="https://4e77834d874b4a8fb0b2153feb49c82d@o105229.ingest.sentry.io/6238005",
    integrations=[DjangoIntegration()],

    traces_sample_rate=1.0,
    send_default_pii=True
)
