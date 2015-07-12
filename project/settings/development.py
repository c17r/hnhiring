from defaults import *

DEBUG = True

INSTALLED_APPS = ('django_extensions',) + INSTALLED_APPS

WSGI_APPLICATION = 'project.wsgi.development.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', 'hnhiring.db'),
    }
}
