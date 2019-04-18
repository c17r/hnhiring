#!/bin/sh

date

echo Who\'s Hiring Refresh
/venv/bin/python /code/manage.py refresh_data -u whoishiring

echo Job Feed Refresh
/venv/bin/python /code/manage.py job_feed

echo Static Pages:
/venv/bin/python /code/manage.py staticsitegen
