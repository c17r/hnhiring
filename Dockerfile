FROM python:3.6.8-alpine AS base

RUN apk update \
&& apk upgrade \
&& apk add --no-cache git uwsgi-python3 \
&& python3 -m venv /venv \
&& /venv/bin/pip install --quiet --no-cache-dir -U pip

EXPOSE 8000

ENV \
PYTHONUNBUFFERED=1 \
UWSGI_GID=2000 \
UWSGI_HTTP_AUTO_CHUNKED=1 \
UWSGI_HTTP_KEEPALIVE=1 \
UWSGI_HTTP_SOCKET=0.0.0.0:8000 \
UWSGI_LAZY_APPS=1 \
UWSGI_MASTER=1 \
UWSGI_PLUGINS=python3 \
UWSGI_THREADS=3 \
UWSGI_UID=1000 \
UWSGI_VIRTUALENV=/venv \
UWSGI_WORKERS=1 \
UWSGI_WSGI_ENV_BEHAVIOR=holy

FROM base AS dependencies

ADD _requirements/prod.txt /requirements.txt

RUN /venv/bin/pip install --quiet --no-cache-dir -r /requirements.txt \
&& mkdir /code/

FROM dependencies AS app

ENV \
DJANGO_SETTINGS_MODULE=_project.settings.live \
UWSGI_CHECK_STATIC=/data/cache/ \
UWSGI_STATIC_MAP="/static/=/code/_project/static/" \
UWSGI_WSGI_FILE=_project/wsgi.py

WORKDIR /code/
ADD . /code/

RUN /venv/bin/python manage.py collectstatic --noinput \
&& (crontab -l | { cat; echo "*/30 * * * * /code/periodic/update.sh > /data/logs/cron.log 2>&1"; } | crontab -)

ENTRYPOINT ["/code/docker-entry.sh"]
CMD ["uwsgi"]
