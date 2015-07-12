from defaults import *

DEBUG = False

TEMPLATE_DEBUG = False

WSGI_APPLICATION = 'project.wsgi.live.application'

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
