#!/bin/sh
set -e

mkdir -p /data/logs/

pgrep -x "crond" > /dev/null || crond

/venv/bin/python manage.py migrate --noinput

exec "$@"
