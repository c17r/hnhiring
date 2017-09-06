from .base import *

DEBUG = False

INSTALLED_APPS = PROD_APPS

ALLOWED_HOSTS = [
    'hnhiring.endrun.org',
    'hnhiring.c17r.com',
    'testserver',  # needed for django_medusa
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/hiring/hnhiring.db',
    }
}
