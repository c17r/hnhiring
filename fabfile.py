from datetime import datetime
from fabric.api import task, env, settings, cd, sudo, run, local, put, path, shell_env

stamp = datetime.now().strftime("v%Y%m%d%H%M%S")
stamptar = "hnhiring-" + stamp + ".tar"
stampzip = stamptar + ".gz"

env.stamp = stamp
env.stamptar = stamptar
env.stampzip = stampzip
env.nginx = "/usr/sbin/nginx"
env.supervisor = "/usr/bin/supervisorctl"

@task
def live():
    env.env = "live"
    env.hosts = [
        "crow.endrun.org"
    ]

@task
def deploy():
    local('find . \( -name "*.pyc" -or -name "*.pyo" -or -name "*py.class" \) -delete')

    local("tar cf %(stamptar)s _requirements/" % env)
    local("tar rf %(stamptar)s _project/" % env)
    local("tar rf %(stamptar)s app/" % env)
    local("tar rf %(stamptar)s manage.py" % env)
    local("tar rf %(stamptar)s gunicorn.conf.py" % env)
    local("gzip %(stamptar)s" % env)

    put(stampzip, "/tmp/%(stampzip)s" % env)

    local("rm %(stampzip)s" % env)

    with settings(sudo_user="hiring"):

        with cd("/home/hiring/web"):
            sudo("mkdir -p %(stamp)s/src" % env)
            sudo("mkdir -p %(stamp)s/venv" % env)

        with cd("/home/hiring/web/%(stamp)s/" % env):
            sudo("tar xfz /tmp/%(stampzip)s -C ./src/" % env)
            sudo("perl -pi -e 's/base/%(env)s/ig' src/manage.py" % env)

            with shell_env(PATH='/opt/pyenv/bin/:$PATH', PYENV_ROOT='/opt/pyenv'):
                sudo("virtualenv venv -p $(pyenv prefix 3.6.1)/bin/python")

            with path("./venv/bin", behavior="prepend"):
                sudo("pip install --quiet --no-cache-dir -r ./src/_requirements/prod.txt")
                sudo("python src/manage.py migrate")
                sudo("python src/manage.py collectstatic --noinput")
                sudo("python src/manage.py staticsitegen")

        with cd("/home/hiring/web"):
            sudo("ln -nsf $(basename $(readlink -f current)) previous")
            sudo("ln -nsf %(stamp)s current" % env)

    sudo("%(supervisor)s restart hnhiring" % env)
    sudo("%(nginx)s -s reload" % env)

    sudo("rm /tmp/%(stampzip)s" % env)

@task
def prune():
    with settings(sudo_user="hiring"):
        with cd("/home/hiring/web"):
            sudo('[ -h current ] && $(for dir in $(ls -1f | grep -e "/$" | grep -ve "$(readlink previous)\|$(readlink current)"); do rm -r $dir; done) || true')
