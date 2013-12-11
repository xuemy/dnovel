#!/usr/bin/python
# -*- coding: utf-8 -*-
from fabric.context_managers import hide, settings
from fabric.operations import sudo, local, run
from fabric.utils import puts
from fabric.api import env,task,prefix
import os

__author__ = 'meng'



env.django_user="django_user"
env.django_user_home=os.path.join("/opt",env.django_user)
env.virtualenv_home = os.path.join(env.django_user_home,'dnovel')

def vagrant():
    env.user='vagrant'
    env.hosts=['127.0.0.1:2222']
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1].strip('\"')
def uname():
    run('uname -a')



def add_task(name, timespec, user, command, environment=None):
    """
    Add a cron task.

    The *command* will be run as *user* periodically.

    You can use any valid `crontab(5)`_ *timespec*, including the
    ``@hourly``, ``@daily``, ``@weekly``, ``@monthly`` and ``@yearly``
    shortcuts.

    You can also provide an optional dictionary of environment variables
    that should be set when running the periodic command.

    Examples::

        from fabtools.cron import add_task

        # Run every month
        add_task('cleanup', '@monthly', 'alice', '/home/alice/bin/cleanup.sh')

        # Run every tuesday and friday at 5:30am
        add_task('reindex', '30 5 * * 2,4', 'bob', '/home/bob/bin/reindex.sh')

    .. _crontab(5): http://manpages.debian.net/cgi-bin/man.cgi?query=crontab&sektion=5

    """
    if environment is None:
        environment = {}

    with NamedTemporaryFile() as script:

        # Write optional environment variables first
        for key, value in environment.iteritems():
            script.write('%(key)s=%(value)s\n' % locals())

        # Write the main crontab line
        script.write('%(timespec)s %(user)s %(command)s\n' % locals())

        script.flush()

        # Upload file
        filename = '/etc/cron.d/%(name)s' % locals()
        upload_template(
            filename=script.name,
            destination=filename,
            context={},
            chown=True,
            use_sudo=True,
        )

        # Fix permissions
        run_as_root('chmod 0644 %s' % filename)

def create_user():
    with settings(hide("running","stdout","stderr","warnings"),warn_only=True):
        res = sudo('useradd -d %(django_user_home)s -m -r %(django_user)s' % env)
    if 'already exists' in res:
        puts('User \'%(django_user)s\' already exists')
        return
    sudo ('passwd %(django_user)s ' % env)

def install_dependencise():
    packages = [
        "python-dev",
        "libxml2-dev",
        'libxslt-dev',
        'python-pip',
        'supervisor',
        'nginx',
        'vim'
    ]
    sudo("apt-get update")
    sudo("apt-get -y install %s" % " ".join(packages))
    if "packages" in env and env.packages:
        sudo("apt-get -y install %s"% " ".join(env.packages))
    sudo("pip install --upgrade pip")

def install_virtualenv():
    sudo("pip install virtualenv")

def create_virtualenv():
    sudo("virtualenv %(virtualenv_home)s"%env)

def virtualenv(command):

    with prefix("source %s/bin/active" % env.virtualenv_home):
        run(command)

def install_requirements():
    #virtualenv("pip install -r django")
    activate = 'source %s/bin/activate' % env.virtualenv_home
    sudo(activate + ' && ' + "pip install django")
    #sudo("source %s/bin/active" % env.virtualenv_home  +'&&' +"pip install django")

def verify_sudo():
    sudo('cd .')

def setup():
    #create_virtualenv()
    verify_sudo()
    install_requirements()