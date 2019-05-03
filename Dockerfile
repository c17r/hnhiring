FROM c17r/py3-webapp AS base

ADD _requirements/prod.txt /requirements.txt

RUN /venv/bin/pip install --quiet --no-cache-dir -r /requirements.txt

FROM base AS app

ENV \
UWSGI_CHECK_STATIC=/data/cache/ \
UWSGI_STATIC_MAP="/static/=/code/_project/static/" \
UWSGI_WSGI_FILE=_project/wsgi.py

WORKDIR /code/
ADD . /code/

RUN /venv/bin/python manage.py collectstatic --noinput \
&& (crontab -l | { cat; echo "*/30 * * * * /code/periodic/update.sh > /data/logs/cron.log 2>&1"; } | crontab -)

ENTRYPOINT ["/code/docker-entry.sh"]
CMD ["uwsgi"]
