
init:
	pip install --upgrade pip-tools
	pip-sync _requirements/dev.txt

reqs:
	pip-compile -U -o _requirements/prod.txt _requirements/prod.in
	pip-compile -U -o _requirements/dev.txt _requirements/prod.in _requirements/dev.in
	pip-sync _requirements/dev.txt

notebook:
	pushd _jupyter && jupyter-notebook && popd

server:
	./manage.py runserver_plus

db-reset:
	[ -f db.sqlite3 ] && rm db.sqlite3 || true
	./manage.py makemigrations
	./manage.py migrate
	./manage.py refresh_data
	./manage.py job_feed

statics:
	./manage.py staticsitegen
