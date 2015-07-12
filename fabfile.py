from datetime import datetime
from fabric.api import task, env, settings, cd, sudo, run, local, put, path

stamp = datetime.now().strftime("v%Y%m%d%H%M%S")
stamptar = "hnhiring-" + stamp + ".tar"
stampzip = stamptar + ".gz"

env.stamp = stamp
env.stamptar = stamptar
env.stampzip = stampzip
env.nginx = "/usr/sbin/nginx"
env.uwsgi = "/usr/bin/uwsgi"

@task
def live():
    env.hosts = [
        "crow.endrun.org"
    ]

@task
def deploy():
    local("pyclean")

    local("tar cf %(stamptar)s app/" % env)
    local("tar rf %(stamptar)s project/" % env)
    local("tar rf %(stamptar)s requirements/" % env)
    local("tar rf %(stamptar)s manage.py" % env)
    local("gzip %(stamptar)s" % env)

    put(stampzip, "/tmp/%(stampzip)s" % env)

    local("rm %(stampzip)s" % env)

    with settings(sudo_user="hiring"):

        with cd("/home/hiring/django"):
            sudo("mkdir -p %(stamp)s/src" % env)
            sudo("mkdir -p %(stamp)s/venv" % env)

        with cd("/home/hiring/django/%(stamp)s/" % env):
            sudo("tar xfz /tmp/%(stampzip)s -C ./src/" % env)
            sudo("rm /tmp/%(stampzip)s" % env)
            sudo("virtualenv venv")

            with path("./venv/bin", behavior="prepend"):
                sudo("pip install -r ./src/requirements/default.txt")
                sudo("python src/manage.py migrate")
                sudo("python src/manage.py collectstatic --noinput")
                sudo("python src/manage.py staticsitegen")

        with cd("/home/hiring/django"):
            sudo("ln -nsf $(basename $(readlink -f current)) previous")
            sudo("ln -nsf %(stamp)s current" % env)

    sudo("%(uwsgi)s --reload /etc/uwsgi/apps-enabled/hnhiring.c17r.org.ini" % env)
    sudo("%(nginx)s -s reload" % env)
