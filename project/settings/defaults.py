import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'cz+wa*s4#5eb98ec*ca(9fat^ah96hx67&9=req8^ezgrsjbv-'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INTERNAL_IPS = (
    '0.0.0.0',
    '127.0.0.1',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_medusa',
    'app',
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

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'hnhiring.db',
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/hnhiring/'
STATIC_ROOT = os.path.join(
    BASE_DIR,
    "static"
)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

MEDUSA_RENDERER_CLASS = "django_medusa.renderers.DiskStaticSiteRenderer"
MEDUSA_MULTITHREAD = True
MEDUSA_DEPLOY_DIR = os.path.join(
    BASE_DIR,
    "static",
    "pages"
)
